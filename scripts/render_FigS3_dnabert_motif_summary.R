# Rebuild Supplementary Figure S3: retained DNABERT-derived motif summary.

library(readr)
library(dplyr)
library(ggplot2)

script_path <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", args, value = TRUE)
  if (length(file_arg) > 0) {
    return(normalizePath(sub("^--file=", "", file_arg[[1]])))
  }
  normalizePath("scripts/render_FigS3_dnabert_motif_summary.R", mustWork = FALSE)
}

repo_root <- normalizePath(file.path(dirname(script_path()), ".."), mustWork = TRUE)
trailing <- commandArgs(trailingOnly = TRUE)
input_file <- if (length(trailing) >= 1) trailing[[1]] else file.path(repo_root, "data/results/reproducible_legacy/tables/dnabert_motif_top20.csv")
output_dir <- if (length(trailing) >= 2) trailing[[2]] else file.path(repo_root, "docs/fig")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

output_png <- file.path(output_dir, "FigS3_dnabert_motif_summary.png")
output_pdf <- file.path(output_dir, "FigS3_dnabert_motif_summary.pdf")

df <- read_csv(input_file, show_col_types = FALSE)

df_plot <- df %>%
  arrange(desc(num_instances)) %>%
  mutate(motif = factor(motif, levels = rev(motif)))

p <- ggplot(df_plot, aes(x = motif, y = num_instances)) +
  geom_col(fill = "#377EB8", width = 0.75) +
  coord_flip() +
  labs(
    title = "Retained DNABERT-derived motif instances",
    x = "Motif",
    y = "Number of retained motif instances"
  ) +
  theme_classic(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    axis.title = element_text(size = 13),
    axis.text = element_text(size = 11),
    plot.margin = margin(10, 20, 10, 10)
  )

ggsave(output_png, p, width = 6, height = 6.5, dpi = 600)
ggsave(output_pdf, p, width = 6, height = 6.5, device = cairo_pdf)

message("Wrote: ", output_png)
message("Wrote: ", output_pdf)
