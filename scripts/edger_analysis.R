#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

count_file <- args[1]
metadata_file <- args[2]
output_dir <- args[3]

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

library(edgeR)

# -----------------------------
# Read data
# -----------------------------

counts <- read.csv(
    count_file,
    row.names = 1,
    check.names = FALSE,
    stringsAsFactors = FALSE
)

# Force numeric conversion
counts[] <- lapply(counts, as.numeric)

# Replace NA generated during conversion
counts[is.na(counts)] <- 0

cat("Total NA values:\n")
print(sum(is.na(counts)))

cat("Storage mode:\n")
str(counts)

cat("Rows with NA:\n")
print(rownames(counts)[apply(is.na(counts), 1, any)])

metadata <- read.csv(
    metadata_file,
    stringsAsFactors = TRUE
)

# -----------------------------
# DEBUG
# -----------------------------

cat("========== DEBUG ==========\n")

cat("Counts dimensions:\n")
print(dim(counts))

cat("Counts column names:\n")
print(colnames(counts))

cat("Metadata:\n")
print(metadata)

cat("Metadata sample IDs:\n")
print(metadata$sample_id)

# -----------------------------
# Match sample order safely
# -----------------------------

common_samples <- intersect(
    colnames(counts),
    metadata$sample_id
)

cat("Common samples:\n")
print(common_samples)

counts <- counts[
    ,
    common_samples,
    drop = FALSE
]

metadata <- metadata[
    match(common_samples, metadata$sample_id),
]

group <- factor(metadata$condition)

cat("Counts after matching:\n")
print(dim(counts))
print(head(counts))

# -----------------------------
# Create DGE object
# -----------------------------

dge <- DGEList(
    counts = counts,
    group = group
)

# -----------------------------
# Filter low-expression genes
# -----------------------------

keep <- filterByExpr(dge)

dge <- dge[keep, , keep.lib.sizes = FALSE]

# -----------------------------
# Normalize
# -----------------------------

dge <- calcNormFactors(dge)

# -----------------------------
# Design matrix
# -----------------------------

design <- model.matrix(~group)

# -----------------------------
# Estimate dispersion
# -----------------------------

dge <- estimateDisp(
    dge,
    design
)

# -----------------------------
# Fit model
# -----------------------------

fit <- glmFit(
    dge,
    design
)

lrt <- glmLRT(
    fit,
    coef = 2
)

# -----------------------------
# Save results
# -----------------------------

results <- topTags(
    lrt,
    n = Inf
)$table

write.csv(
    results,
    file.path(
        output_dir,
        "edger_results.csv"
    )
)

write.csv(
    cpm(
        dge,
        normalized.lib.sizes = TRUE
    ),
    file.path(
        output_dir,
        "normalized_counts.csv"
    )
)

# -----------------------------
# MDS plot
# -----------------------------

png(
    file.path(
        output_dir,
        "MDS_plot.png"
    )
)

plotMDS(
    dge,
    labels = metadata$sample_id
)

dev.off()

# -----------------------------
# BCV plot
# -----------------------------

png(
    file.path(
        output_dir,
        "BCV_plot.png"
    )
)

plotBCV(dge)

dev.off()

cat("edgeR analysis completed.\n")