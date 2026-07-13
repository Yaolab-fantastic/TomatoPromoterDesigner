# Rebuild Supplementary Figure S4: retained k-mer distribution comparison.

library(readr)
library(dplyr)
library(ggplot2)
library(patchwork)

script_path <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", args, value = TRUE)
  if (length(file_arg) > 0) {
    return(normalizePath(sub("^--file=", "", file_arg[[1]])))
  }
  normalizePath("scripts/render_FigS4_kmer_distribution.R", mustWork = FALSE)
}

repo_root <- normalizePath(file.path(dirname(script_path()), ".."), mustWork = TRUE)
trailing <- commandArgs(trailingOnly = TRUE)
input_file <- if (length(trailing) >= 1) trailing[[1]] else file.path(repo_root, "data/results/reproducible_legacy/tables/kmer_frequency_comparison.csv")
output_dir <- if (length(trailing) >= 2) trailing[[2]] else file.path(repo_root, "docs/fig")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

output_png <- file.path(output_dir, "FigS4_kmer_distribution.png")
output_pdf <- file.path(output_dir, "FigS4_kmer_distribution.pdf")

df <- read_csv(input_file, show_col_types = FALSE)

plot_region <- function(data, title_text) {
  r_value <- cor(data$original_frequency, data$generated_frequency, method = "pearson")
  ggplot(data, aes(x = original_frequency, y = generated_frequency)) +
    geom_point(size = 2.5, alpha = 0.75, color = "#756BB1") +
    geom_abline(slope = 1, intercept = 0, linetype = "dashed", linewidth = 0.8, color = "grey45") +
    annotate(
      "text",
      x = Inf,
      y = Inf,
      label = paste0("Pearson r = ", sprintf("%.3f", r_value)),
      hjust = 1.1,
      vjust = 1.5,
      size = 4
    ) +
    labs(
      title = title_text,
      x = "Original promoter frequency",
      y = "Generated promoter frequency"
    ) +
    theme_classic(base_size = 13) +
    theme(plot.title = element_text(hjust = 0.5, face = "bold", size = 15))
}

all_df <- df %>% filter(grepl("^all$", region, ignore.case = TRUE))
prox_df <- df %>% filter(grepl("prox", region, ignore.case = TRUE))
dist_df <- df %>% filter(grepl("dist", region, ignore.case = TRUE))

final_plot <- plot_region(all_df, "All") +
  plot_region(prox_df, "Proximal 20 bp") +
  plot_region(dist_df, "Distal 20 bp") +
  plot_layout(ncol = 3)

ggsave(output_png, final_plot, width = 12, height = 4, dpi = 600)
ggsave(output_pdf, final_plot, width = 12, height = 4, device = cairo_pdf)

message("Wrote: ", output_png)
message("Wrote: ", output_pdf)
