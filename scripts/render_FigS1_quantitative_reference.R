# Rebuild Supplementary Figure S1: retained quantitative reference.

library(ggplot2)
library(readr)

script_path <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", args, value = TRUE)
  if (length(file_arg) > 0) {
    return(normalizePath(sub("^--file=", "", file_arg[[1]])))
  }
  normalizePath("scripts/render_FigS1_quantitative_reference.R", mustWork = FALSE)
}

repo_root <- normalizePath(file.path(dirname(script_path()), ".."), mustWork = TRUE)
trailing <- commandArgs(trailingOnly = TRUE)
input_file <- if (length(trailing) >= 1) trailing[[1]] else file.path(repo_root, "data/raw/mpravae/generated_prediction_results.csv")
output_dir <- if (length(trailing) >= 2) trailing[[2]] else file.path(repo_root, "docs/fig")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

output_png <- file.path(output_dir, "FigS1_quantitative_reference.png")
output_pdf <- file.path(output_dir, "FigS1_quantitative_reference.pdf")

df <- read_csv(input_file, show_col_types = FALSE)
df <- df[complete.cases(df[, c("Predicted_Expr", "True_Expr")]), ]
df <- df[is.finite(df$Predicted_Expr) & is.finite(df$True_Expr), ]

n_pairs <- nrow(df)
pearson_r <- cor(df$Predicted_Expr, df$True_Expr, method = "pearson")
stat_text <- paste0("n = ", format(n_pairs, big.mark = ","), "\nPearson r = ", sprintf("%.3f", pearson_r))

p <- ggplot(df, aes(x = True_Expr, y = Predicted_Expr)) +
  geom_point(size = 0.35, alpha = 0.25, color = "#1F9E89") +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", linewidth = 1.0, color = "#E64B35") +
  annotate(
    "text",
    x = min(df$True_Expr, na.rm = TRUE),
    y = max(df$Predicted_Expr, na.rm = TRUE),
    label = stat_text,
    hjust = 0,
    vjust = 1,
    size = 5,
    color = "#333333"
  ) +
  labs(
    x = "True scalar-expression value",
    y = "Predicted scalar-expression value"
  ) +
  theme_classic(base_size = 14) +
  theme(
    axis.title = element_text(size = 15, face = "bold"),
    axis.text = element_text(size = 12),
    axis.line = element_line(linewidth = 0.6),
    plot.margin = margin(10, 10, 10, 10)
  )

ggsave(output_png, p, width = 5, height = 5, dpi = 300, units = "in")
ggsave(output_pdf, p, width = 5, height = 5, units = "in")

message("Wrote: ", output_png)
message("Wrote: ", output_pdf)
