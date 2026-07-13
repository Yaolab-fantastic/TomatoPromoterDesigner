# Rebuild Supplementary Figure S2: retained tissue-associated expression heatmap.

library(readr)
library(dplyr)
library(pheatmap)
library(grid)

script_path <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", args, value = TRUE)
  if (length(file_arg) > 0) {
    return(normalizePath(sub("^--file=", "", file_arg[[1]])))
  }
  normalizePath("scripts/render_FigS2_expression_heatmap.R", mustWork = FALSE)
}

repo_root <- normalizePath(file.path(dirname(script_path()), ".."), mustWork = TRUE)
trailing <- commandArgs(trailingOnly = TRUE)
input_file <- if (length(trailing) >= 1) trailing[[1]] else file.path(repo_root, "data/results/reproducible_legacy/tables/expression_heatmap_source.csv")
output_dir <- if (length(trailing) >= 2) trailing[[2]] else file.path(repo_root, "docs/fig")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

output_png <- file.path(output_dir, "FigS2_expression_heatmap.png")
output_pdf <- file.path(output_dir, "FigS2_expression_heatmap.pdf")

df <- read_csv(input_file, show_col_types = FALSE)

df_order <- df %>%
  arrange(preferred_tissue, desc(target_margin)) %>%
  mutate(promoter_index = row_number())

heatmap_matrix <- df_order %>%
  select(expr_root, expr_stem, expr_leaf, expr_fruit) %>%
  as.matrix()

rownames(heatmap_matrix) <- as.character(df_order$promoter_index)
colnames(heatmap_matrix) <- c("Root", "Stem", "Leaf", "Fruit")

row_annotation <- data.frame(Preferred_tissue = df_order$preferred_tissue)
rownames(row_annotation) <- rownames(heatmap_matrix)

heat_colors <- colorRampPalette(c("#FFF7BC", "#FEC44F", "#F16913", "#B30000"))(100)

heatmap_plot <- pheatmap(
  heatmap_matrix,
  color = heat_colors,
  cluster_rows = FALSE,
  cluster_cols = FALSE,
  scale = "none",
  border_color = NA,
  annotation_row = row_annotation,
  show_rownames = FALSE,
  show_colnames = TRUE,
  fontsize_col = 12,
  angle_col = 0,
  legend = TRUE,
  main = "Retained tissue-associated expression profiles",
  silent = TRUE
)

pdf(output_pdf, width = 5.5, height = 12, useDingbats = FALSE)
grid.newpage()
grid.draw(heatmap_plot$gtable)
dev.off()

png(output_png, width = 1800, height = 3600, res = 300)
grid.newpage()
grid.draw(heatmap_plot$gtable)
dev.off()

message("Wrote: ", output_png)
message("Wrote: ", output_pdf)
