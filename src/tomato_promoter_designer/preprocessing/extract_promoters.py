from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PromoterWindow:
    chromosome: str
    gene_id: str
    strand: str
    start: int
    end: int


def upstream_window(gene_start: int, window_size: int = 165) -> tuple[int, int]:
    if gene_start <= 1:
        raise ValueError("Gene start must be positive.")
    promoter_end = gene_start - 1
    promoter_start = max(1, promoter_end - window_size + 1)
    return promoter_start, promoter_end

