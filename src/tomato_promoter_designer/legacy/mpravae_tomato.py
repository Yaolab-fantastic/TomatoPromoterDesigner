from __future__ import annotations

import random
import re
import os
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

from tomato_promoter_designer.io.schema import DesignResult, PredictionResult, SequenceRecord


BASES = ("A", "C", "G", "T")
BASE_TO_INDEX = {base: index for index, base in enumerate(BASES)}
TISSUE_ORDER = ("root", "stem", "leaf", "fruit")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _default_models_dir() -> Path:
    override = os.environ.get("TOMATO_PROMOTER_DESIGNER_MODELS_DIR")
    if override:
        return Path(override)
    repo_models = _repo_root() / "models"
    if repo_models.exists():
        return repo_models
    return Path.cwd() / "models"


DEFAULT_MPRAVAE_CHECKPOINT = _default_models_dir() / "mpravae" / "best_val_corr_model.pth"

_TATA_PATTERN = re.compile(r"TATA[AT]A[AT]")
TOMATO_GC_RANGE = (0.12, 0.52)
TOMATO_MAX_HOMOPOLYMER = 13


def one_hot_encode(sequence: str) -> torch.Tensor:
    mapping = {
        "A": (1.0, 0.0, 0.0, 0.0),
        "C": (0.0, 1.0, 0.0, 0.0),
        "G": (0.0, 0.0, 1.0, 0.0),
        "T": (0.0, 0.0, 0.0, 1.0),
    }
    encoded = []
    for base in sequence.upper():
        if base not in mapping:
            raise ValueError(
                "Legacy MpraVAE adapter only supports unambiguous A/C/G/T input. "
                f"Found unsupported base {base!r}."
            )
        encoded.append(mapping[base])
    return torch.tensor(encoded, dtype=torch.float32).transpose(0, 1)


def decode_one_hot(tensor: torch.Tensor) -> str:
    indices = tensor.argmax(dim=0).tolist()
    return "".join(BASES[index] for index in indices)


def softplus_scores(raw_scores: torch.Tensor) -> torch.Tensor:
    return F.softplus(raw_scores)


def gc_fraction(sequence: str) -> float:
    return (sequence.count("G") + sequence.count("C")) / max(len(sequence), 1)


def max_homopolymer_length(sequence: str) -> int:
    if not sequence:
        return 0
    best = 1
    run = 1
    for previous, current in zip(sequence, sequence[1:]):
        if previous == current:
            run += 1
            best = max(best, run)
        else:
            run = 1
    return best


def midpoint_window(sequence: str) -> str:
    midpoint = len(sequence) // 2
    return sequence[max(0, midpoint - 45) : max(0, midpoint - 15)]


def promoter_qc_summary(
    sequence: str,
    gc_range: tuple[float, float] = TOMATO_GC_RANGE,
    max_poly: int = TOMATO_MAX_HOMOPOLYMER,
) -> dict[str, object]:
    window = midpoint_window(sequence)
    gc = (sequence.count("G") + sequence.count("C")) / max(len(sequence), 1)
    max_homopolymer = max_homopolymer_length(sequence)
    tata_like_window = _TATA_PATTERN.search(window) is not None
    window_at_fraction = (window.count("A") + window.count("T")) / max(len(window), 1)
    passes = gc_range[0] <= gc <= gc_range[1] and max_homopolymer <= max_poly
    return {
        "passes": passes,
        "gc_fraction": round(gc, 4),
        "max_homopolymer": max_homopolymer,
        "tata_like_window": tata_like_window,
        "window_at_fraction": round(window_at_fraction, 4),
    }


def is_promoter_like(
    sequence: str,
    gc_range: tuple[float, float] = TOMATO_GC_RANGE,
    max_poly: int = TOMATO_MAX_HOMOPOLYMER,
) -> bool:
    return bool(promoter_qc_summary(sequence, gc_range=gc_range, max_poly=max_poly)["passes"])


def sample_sequence(decoded_probs: torch.Tensor, rng: random.Random, greedy: bool = False) -> str:
    if greedy:
        return decode_one_hot(decoded_probs)

    letters: list[str] = []
    for position in range(decoded_probs.shape[1]):
        probabilities = decoded_probs[:, position].tolist()
        draw = rng.random()
        cumulative = 0.0
        chosen_index = len(BASES) - 1
        for index, probability in enumerate(probabilities):
            cumulative += float(probability)
            if draw <= cumulative:
                chosen_index = index
                break
        letters.append(BASES[chosen_index])
    return "".join(letters)


def count_point_mutations(original_sequence: str, designed_sequence: str) -> int:
    return sum(original != designed for original, designed in zip(original_sequence, designed_sequence))


def selected_base_confidences(decoded_probs: torch.Tensor, sequence: str) -> list[float]:
    return [float(decoded_probs[BASE_TO_INDEX[base], index]) for index, base in enumerate(sequence)]


class VAEEncoder(nn.Module):
    def __init__(self, latent_dim: int = 64) -> None:
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(4, 32, kernel_size=7, padding=3),
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Conv1d(32, 64, kernel_size=7, padding=3),
            nn.ReLU(),
            nn.Flatten(),
        )
        with torch.no_grad():
            dummy_out = self.conv(torch.zeros(1, 4, 165))
        self.flat_dim = dummy_out.shape[1]
        self.fc_mu = nn.Linear(self.flat_dim, latent_dim)
        self.fc_logvar = nn.Linear(self.flat_dim, latent_dim)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        encoded = self.conv(x)
        mu = self.fc_mu(encoded)
        logvar = self.fc_logvar(encoded)
        std = torch.exp(0.5 * logvar)
        z = mu + torch.randn_like(std) * std
        return z, mu, logvar


class VAEDecoder(nn.Module):
    def __init__(self, latent_dim: int = 64, flat_dim: int = 5248) -> None:
        super().__init__()
        self.flat_dim = flat_dim
        self.fc = nn.Linear(latent_dim, flat_dim)
        self.unflatten_shape = self._infer_unflatten_shape()
        self.decoder = nn.Sequential(
            nn.Unflatten(1, self.unflatten_shape),
            nn.ConvTranspose1d(self.unflatten_shape[0], 128, kernel_size=7, padding=3),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.ConvTranspose1d(128, 128, kernel_size=7, padding=3),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.ConvTranspose1d(128, 64, kernel_size=7, padding=3),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.ConvTranspose1d(64, 32, kernel_size=7, padding=3),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.ConvTranspose1d(32, 16, kernel_size=7, padding=3),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Upsample(size=165),
            nn.ConvTranspose1d(16, 4, kernel_size=7, padding=3),
            nn.Softmax(dim=1),
        )

    def _infer_unflatten_shape(self) -> tuple[int, int]:
        for channels in (64, 128, 32, 16):
            if self.flat_dim % channels == 0:
                return channels, self.flat_dim // channels
        raise ValueError(f"Cannot infer unflatten shape from flat_dim={self.flat_dim}")

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        latent = self.fc(z)
        return self.decoder(latent)


class ExpressionPredictor(nn.Module):
    def __init__(self, latent_dim: int = 64, num_tissues: int = 4) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_tissues),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return self.net(z)


class JointPromoterModel(nn.Module):
    def __init__(self, latent_dim: int = 64, num_tissues: int = 4) -> None:
        super().__init__()
        self.encoder = VAEEncoder(latent_dim=latent_dim)
        self.decoder = VAEDecoder(latent_dim=latent_dim, flat_dim=self.encoder.flat_dim)
        self.predictor = ExpressionPredictor(latent_dim=latent_dim, num_tissues=num_tissues)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        z, mu, logvar = self.encoder(x)
        predicted = self.predictor(z)
        reconstructed = self.decoder(z)
        return reconstructed, mu, logvar, predicted


class MpraVAETomatoAdapter:
    """Clean adapter around the tomato multi-tissue VAE + predictor checkpoint."""

    def __init__(
        self,
        checkpoint_path: str | Path | None = None,
        device: str = "cpu",
        latent_dim: int = 64,
    ) -> None:
        self.checkpoint_path = Path(checkpoint_path or DEFAULT_MPRAVAE_CHECKPOINT)
        self.device = torch.device(device)
        self.latent_dim = latent_dim
        self.model = self._load_model()

    def _load_model(self) -> JointPromoterModel:
        if not self.checkpoint_path.exists():
            raise FileNotFoundError(f"MpraVAE checkpoint not found: {self.checkpoint_path}")
        model = JointPromoterModel(latent_dim=self.latent_dim, num_tissues=4)
        state_dict = torch.load(self.checkpoint_path, map_location=self.device)
        model.load_state_dict(state_dict, strict=True)
        model = model.to(self.device)
        model.eval()
        return model

    def _tensorize(self, record: SequenceRecord) -> torch.Tensor:
        return one_hot_encode(record.sequence).unsqueeze(0).to(self.device)

    def _predict_scores(self, input_tensor: torch.Tensor) -> dict[str, float]:
        with torch.no_grad():
            _, mu, _ = self.model.encoder(input_tensor)
            raw_scores = self.model.predictor(mu)
            scores = softplus_scores(raw_scores)[0].detach().cpu().tolist()
        return dict(zip(TISSUE_ORDER, [round(float(score), 6) for score in scores]))

    def _predict_one(self, record: SequenceRecord) -> PredictionResult:
        tissue_scores = self._predict_scores(self._tensorize(record))
        preferred_tissue = max(tissue_scores, key=tissue_scores.get)
        return PredictionResult(
            sequence_id=record.sequence_id,
            sequence=record.sequence,
            expr_root=tissue_scores["root"],
            expr_stem=tissue_scores["stem"],
            expr_leaf=tissue_scores["leaf"],
            expr_fruit=tissue_scores["fruit"],
            preferred_tissue=preferred_tissue,
        )

    def predict(self, records: list[SequenceRecord]) -> list[PredictionResult]:
        results: list[PredictionResult] = []
        for record in records:
            results.append(self._predict_one(record))
        return results

    def design(
        self,
        records: list[SequenceRecord],
        target_tissue: str,
        candidates: int = 5,
        seed: int = 42,
        steps: int = 400,
        learning_rate: float = 0.05,
        gamma: float = 0.05,
        beta: float = 0.1,
        hi_lim: float = 10.0,
    ) -> list[DesignResult]:
        if target_tissue not in TISSUE_ORDER:
            raise ValueError(f"Unsupported target tissue: {target_tissue}")

        rng = random.Random(seed)
        torch_generator = torch.Generator(device=self.device.type)
        torch_generator.manual_seed(seed)
        target_index = TISSUE_ORDER.index(target_tissue)
        designs: list[DesignResult] = []
        for record in records:
            designs.extend(
                self._design_one(
                    record=record,
                    target_index=target_index,
                    target_tissue=target_tissue,
                    candidates=candidates,
                    rng=rng,
                    steps=steps,
                    learning_rate=learning_rate,
                    gamma=gamma,
                    beta=beta,
                    hi_lim=hi_lim,
                    torch_generator=torch_generator,
                )
            )
        return designs

    def _repair_candidate_sequence(
        self,
        decoded_probs: torch.Tensor,
        candidate_sequence: str,
        original_sequence: str,
    ) -> tuple[str, str, bool]:
        if is_promoter_like(candidate_sequence):
            return candidate_sequence, "mpravae_decoded", True

        confidences = selected_base_confidences(decoded_probs, candidate_sequence)
        repaired = list(candidate_sequence)
        changed_positions = [
            index for index, (candidate_base, original_base) in enumerate(zip(candidate_sequence, original_sequence))
            if candidate_base != original_base
        ]
        changed_positions.sort(key=lambda index: confidences[index])

        for position in changed_positions:
            repaired[position] = original_sequence[position]
            repaired_sequence = "".join(repaired)
            if is_promoter_like(repaired_sequence):
                return repaired_sequence, "mpravae_repaired_by_reversion", True

        return original_sequence, "mpravae_qc_fallback", is_promoter_like(original_sequence)

    def _design_one(
        self,
        record: SequenceRecord,
        target_index: int,
        target_tissue: str,
        candidates: int,
        rng: random.Random,
        steps: int,
        learning_rate: float,
        gamma: float,
        beta: float,
        hi_lim: float,
        torch_generator: torch.Generator,
    ) -> list[DesignResult]:
        x_tensor = self._tensorize(record)
        with torch.no_grad():
            _, z0, _ = self.model.encoder(x_tensor)

        attempt_budget = max(candidates * 6, 12)
        all_candidates: list[tuple[float, DesignResult]] = []
        unique_candidates: dict[str, tuple[float, DesignResult]] = {}
        for attempt_index in range(1, attempt_budget + 1):
            noise = torch.randn(z0.shape, generator=torch_generator, device=z0.device) * (0.04 + 0.01 * attempt_index)
            z = z0.clone().detach() + noise
            z.requires_grad_(True)
            optimizer = torch.optim.Adam([z], lr=learning_rate)

            for _ in range(steps):
                optimizer.zero_grad()
                raw_scores = self.model.predictor(z)
                scores = softplus_scores(raw_scores)
                target_score = scores[0, target_index]
                competitor_indices = [index for index in range(len(TISSUE_ORDER)) if index != target_index]
                competitor_max = torch.max(scores[0, competitor_indices])
                gap = target_score - competitor_max
                loss = -gap + gamma * torch.norm(z - z0) ** 2 + beta * F.relu(scores - hi_lim).sum()
                loss.backward()
                optimizer.step()

            decoded_probs = self.model.decoder(z)[0].detach().cpu()
            sampled_sequence = sample_sequence(decoded_probs, rng=rng, greedy=attempt_index == 1)
            designed_sequence, design_status, qc_pass = self._repair_candidate_sequence(
                decoded_probs=decoded_probs,
                candidate_sequence=sampled_sequence,
                original_sequence=record.sequence,
            )
            prediction = self._predict_one(SequenceRecord(record.sequence_id, designed_sequence))
            score_map = {
                "root": prediction.expr_root,
                "stem": prediction.expr_stem,
                "leaf": prediction.expr_leaf,
                "fruit": prediction.expr_fruit,
            }
            ranking_score = score_map[target_tissue] - max(
                score_map[tissue] for tissue in TISSUE_ORDER if tissue != target_tissue
            )
            design = DesignResult(
                sequence_id=record.sequence_id,
                target_tissue=target_tissue,
                candidate_rank=attempt_index,
                original_sequence=record.sequence,
                designed_sequence=designed_sequence,
                expr_root=score_map["root"],
                expr_stem=score_map["stem"],
                expr_leaf=score_map["leaf"],
                expr_fruit=score_map["fruit"],
                preserved_motifs="not_tracked",
                design_status=design_status,
                num_mutations=count_point_mutations(record.sequence, designed_sequence),
                passes_qc=qc_pass,
            )
            all_candidates.append((ranking_score, design))
            best_so_far = unique_candidates.get(designed_sequence)
            if best_so_far is None or ranking_score > best_so_far[0]:
                unique_candidates[designed_sequence] = (ranking_score, design)

            if len(unique_candidates) >= candidates and attempt_index >= max(candidates * 2, 6):
                break

        pool = sorted(unique_candidates.values(), key=lambda item: item[0], reverse=True)
        if len(pool) < candidates:
            for candidate in sorted(all_candidates, key=lambda item: item[0], reverse=True):
                if len(pool) >= candidates:
                    break
                pool.append(candidate)

        ranked: list[DesignResult] = []
        for output_rank, (_, design) in enumerate(pool[:candidates], start=1):
            ranked.append(
                DesignResult(
                    sequence_id=design.sequence_id,
                    target_tissue=design.target_tissue,
                    candidate_rank=output_rank,
                    original_sequence=design.original_sequence,
                    designed_sequence=design.designed_sequence,
                    expr_root=design.expr_root,
                    expr_stem=design.expr_stem,
                    expr_leaf=design.expr_leaf,
                    expr_fruit=design.expr_fruit,
                    preserved_motifs=design.preserved_motifs,
                    design_status=design.design_status,
                    num_mutations=design.num_mutations,
                    passes_qc=design.passes_qc,
                )
            )
        return ranked
