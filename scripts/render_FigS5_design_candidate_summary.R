# Rebuild Supplementary Figure S5: retained design candidate summaries.

library(ggplot2)
library(readr)
library(dplyr)
library(patchwork)

script_path <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", args, value = TRUE)
  if (length(file_arg) > 0) {
    return(normalizePath(sub("^--file=", "", file_arg[[1]])))
  }
  normalizePath("scripts/render_FigS5_design_candidate_summary.R", mustWork = FALSE)
}

repo_root <- normalizePath(file.path(dirname(script_path()), ".."), mustWork = TRUE)
trailing <- commandArgs(trailingOnly = TRUE)
input_file <- if (length(trailing) >= 1) trailing[[1]] else file.path(repo_root, "data/results/reproducible_legacy/tables/design_candidate_summary.csv")
output_dir <- if (length(trailing) >= 2) trailing[[2]] else file.path(repo_root, "docs/fig")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

output_png <- file.path(output_dir, "FigS5_design_candidate_summary.png")
output_pdf <- file.path(output_dir, "FigS5_design_candidate_summary.pdf")

df <- read_csv(input_file, show_col_types = FALSE)

pA <- ggplot(df, aes(x = "Designed promoter candidates", y = pred_fruit)) +
  geom_violin(fill = "#7B61A8", color = "#5E3C99", alpha = 0.35, linewidth = 1) +
  geom_jitter(width = 0.08, size = 1.8, alpha = 0.35, color = "#5E3C99") +
  geom_hline(yintercept = median(df$pred_fruit), linetype = "dashed", linewidth = 0.8) +
  annotate("text", x = 1, y = median(df$pred_fruit), label = paste0("median = ", round(median(df$pred_fruit), 2)), hjust = -0.05, vjust = -0.6, size = 4) +
  labs(x = NULL, y = "Predicted fruit-associated score") +
  theme_classic(base_size = 14) +
  theme(axis.text.x = element_blank(), axis.ticks.x = element_blank())

pB <- ggplot(df, aes(x = "Designed promoter candidates", y = fruit_margin)) +
  geom_violin(fill = "#E97855", color = "#D84A2F", alpha = 0.35, linewidth = 1) +
  geom_jitter(width = 0.08, size = 1.8, alpha = 0.35, color = "#D84A2F") +
  geom_hline(yintercept = median(df$fruit_margin), linetype = "dashed", linewidth = 0.8) +
  annotate("text", x = 1, y = median(df$fruit_margin), label = paste0("median = ", round(median(df$fruit_margin), 2)), hjust = -0.05, vjust = -0.6, size = 4) +
  labs(x = NULL, y = "Fruit-associated bias margin") +
  theme_classic(base_size = 14) +
  theme(axis.text.x = element_blank(), axis.ticks.x = element_blank())

median_edit <- median(df$num_point_differences, na.rm = TRUE)

pC <- ggplot(df, aes(x = num_point_differences)) +
  geom_histogram(aes(y = after_stat(density)), bins = 30, fill = "#9DD9D2", color = "white", alpha = 0.8) +
  geom_density(linewidth = 1.2, color = "#2A9D8F") +
  geom_vline(xintercept = median_edit, linetype = "dashed", linewidth = 0.9) +
  annotate("text", x = median_edit + 2, y = Inf, label = paste0("median = ", median_edit), vjust = 2, size = 4) +
  labs(x = "Hamming differences from conditioning sequence", y = "Density") +
  theme_classic(base_size = 14)

final_plot <- pA + pB + pC + plot_annotation(tag_levels = "A")

ggsave(output_png, final_plot, width = 12, height = 4.5, dpi = 300)
ggsave(output_pdf, final_plot, width = 12, height = 4.5, device = cairo_pdf)

message("Wrote: ", output_png)
message("Wrote: ", output_pdf)
