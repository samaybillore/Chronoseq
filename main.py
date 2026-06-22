from pathlib import Path
import config
from modules.chronoseq_setup import run_setup
from modules.logger import CHRONOSEQLogger


# --------------------------------------------------
# LOGGER
# --------------------------------------------------

logger = CHRONOSEQLogger(config.LOG_FILE)

logger.info(
    "========== PIPELINE STARTED =========="
)

# --------------------------------------------------
# CHRONOSEQ SETUP
# --------------------------------------------------

logger.stage_start(
    "STAGE 0 : CHRONOSEQ SETUP"
)

print(
    "\n========== STAGE 0 : CHRONOSEQ SETUP ==========\n"
)

run_setup()

# --------------------------------------------------
# Modules Import
# --------------------------------------------------

from modules.reference_finder import find_reference_files
from modules.metadata_loader import load_metadata
from modules.file_scanner import find_fastq_files
from modules.planner import create_processing_plan
from modules.sra_converter import convert_sra_to_fastq
from modules.fastqc_runner import run_fastqc
from modules.multiqc_runner import run_multiqc
from modules.trimmomatic_runner import run_trimmomatic
from modules.bowtie_build import build_bowtie2_index
from modules.bowtie_align import run_bowtie_align
from modules.samtools_runner import run_samtools
from modules.stringtie_runner import run_stringtie
from modules.sample_list_generator import generate_sample_list
from modules.prepde_runner import run_prepde
from modules.native_edger_runner import run_native_edger
from modules.trinity_edger_runner import run_trinity_edger
from modules.trinity_sample_creator import create_trinity_sample_file
from modules.trinity_matrix_converter import convert_gene_matrix_to_tsv
from modules.mapping_stats import generate_mapping_stats
from modules.mapping_summary import generate_mapping_summary
from modules.pca_plot import generate_pca_plot
from modules.volcano_plot import generate_volcano_plot
from modules.heatmap_plot import generate_heatmap
from modules.ma_plot import generate_ma_plot
from modules.html_report import generate_html_report

FASTA, GFF = find_reference_files(
    config.REFERENCE
)

# --------------------------------------------------
# Reference Check
# --------------------------------------------------

print()

# print("=" * 60)
# print("REFERENCE FILES DETECTED")
# print("=" * 60)

# print(f"Genome     : {FASTA.name}")
# print(f"Annotation : {GFF.name}")

# print("=" * 60)

logger.info(
    f"Reference genome: {FASTA.name}"
)

logger.info(
    f"Reference annotation: {GFF.name}"
)

logger.stage_end(
    "STAGE 0 : CHRONOSEQ SETUP"
)

# --------------------------------------------------
# Stage 1 : Load metadata and create processing plan
# --------------------------------------------------

logger.stage_start(
    "STAGE 1 : LOADING METADATA"
)

print(
    "\n========== STAGE 1 : LOADING METADATA ==========\n"
)

metadata = load_metadata(config.METADATA)

files = find_fastq_files(config.RAW)

plan = create_processing_plan(
    metadata,
    files
)

print(plan)

logger.stage_end(
    "STAGE 1 : LOADING METADATA"
)


# --------------------------------------------------
# Stage 2 : SRA -> FASTQ
# --------------------------------------------------

logger.stage_start(
    "STAGE 2 : SRA -> FASTQ"
)

print(
    "\n========== STAGE 2 : SRA -> FASTQ ==========\n"
)

for sample in plan:

    sra_file = Path(sample["file"])

    convert_sra_to_fastq(
        sra_file,
        config.FASTQ
    )

logger.stage_end(
    "STAGE 2 : SRA -> FASTQ"
)


# --------------------------------------------------
# Stage 3 : Raw FastQC
# --------------------------------------------------

logger.stage_start(
    "STAGE 3 : RAW FASTQC"
)

print(
    "\n========== STAGE 3 : RAW FASTQC ==========\n"
)

for sample in plan:

    sample_id = sample["sample_id"]

    fastq_1 = config.FASTQ / f"{sample_id}_1.fastq"
    fastq_2 = config.FASTQ / f"{sample_id}_2.fastq"

    run_fastqc(
        fastq_1,
        config.QC_RAW
    )

    run_fastqc(
        fastq_2,
        config.QC_RAW
    )

logger.stage_end(
    "STAGE 3 : RAW FASTQC"
)

# --------------------------------------------------
# Stage 4 : Raw MultiQC
# --------------------------------------------------

logger.stage_start(
    "STAGE 4 : RAW MULTIQC"
)

print(
    "\n========== STAGE 4 : RAW MULTIQC ==========\n"
)

run_multiqc(
    config.QC_RAW,
    config.MULTIQC_RAW
)

logger.stage_end(
    "STAGE 4 : RAW MULTIQC"
)

# --------------------------------------------------
# Stage 5 : Trimmomatic
# --------------------------------------------------

logger.stage_start(
    "STAGE 5 : TRIMMOMATIC"
)

print(
    "\n========== STAGE 5 : TRIMMOMATIC ==========\n"
)

for sample in plan:

    sample_id = sample["sample_id"]

    fastq_1 = config.FASTQ / f"{sample_id}_1.fastq"
    fastq_2 = config.FASTQ / f"{sample_id}_2.fastq"

    run_trimmomatic(
        fastq_1,
        fastq_2,
        config.TRIMMED,
        config.ADAPTERS
    )

logger.stage_end(
    "STAGE 5 : TRIMMOMATIC"
)

# --------------------------------------------------
# Stage 6 : FastQC on Trimmed Reads
# --------------------------------------------------

logger.stage_start(
    "STAGE 6 : TRIMMED FASTQC"
)

print(
    "\n========== STAGE 6 : TRIMMED FASTQC ==========\n"
)

for sample in plan:

    sample_id = sample["sample_id"]

    paired_1 = config.TRIMMED / f"{sample_id}_1_paired.fq.gz"
    paired_2 = config.TRIMMED / f"{sample_id}_2_paired.fq.gz"

    run_fastqc(
        paired_1,
        config.QC_TRIMMED
    )

    run_fastqc(
        paired_2,
        config.QC_TRIMMED
    )

logger.stage_end(
    "STAGE 6 : TRIMMED FASTQC"
)

# --------------------------------------------------
# Stage 7 : Trimmed MultiQC
# --------------------------------------------------

logger.stage_start(
    "STAGE 7 : TRIMMED MULTIQC"
)

print(
    "\n========== STAGE 7 : TRIMMED MULTIQC ==========\n"
)

run_multiqc(
    config.QC_TRIMMED,
    config.MULTIQC_TRIMMED
)

logger.stage_end(
    "STAGE 7 : TRIMMED MULTIQC"
)

# --------------------------------------------------
# Stage 8 : Build Bowtie2 Index
# --------------------------------------------------

logger.stage_start(
    "STAGE 8 : BOWTIE2 Index"
)

print(
    "\n========== STAGE 8 : BOWTIE2 ==========\n"
)

build_bowtie2_index(
    FASTA,
    config.BOWTIE_INDEX
)

logger.stage_end(
    "STAGE 8 : BOWTIE2 Index"
)

# --------------------------------------------------
# Stage 9 : Bowtie2 Alignment
# --------------------------------------------------

logger.stage_start(
    "STAGE 9 : BOWTIE2 ALIGN"
)

print(
    "\n========== STAGE 9 : BOWTIE2 ALIGN ==========\n"
)

for sample in plan:

    sample_id = sample["sample_id"]

    paired_1 = config.TRIMMED / f"{sample_id}_1_paired.fq.gz"
    paired_2 = config.TRIMMED / f"{sample_id}_2_paired.fq.gz"

    run_bowtie_align(
        paired_1,
        paired_2,
        config.BOWTIE_INDEX,
        config.ALIGNMENTS
    )

logger.stage_end(
    "STAGE 9 : BOWTIE2 ALIGN"
)

# --------------------------------------------------
# Stage 10 : SAMTOOLS
# --------------------------------------------------

logger.stage_start(
    "STAGE 10 : SAMTOOLS"
)

print(
    "\n========== STAGE 10 : SAMTOOLS ==========\n"
)

for sample in plan:

    sample_id = sample["sample_id"]

    sam_file = config.ALIGNMENTS / f"{sample_id}.sam"

    bam_file, sorted_bam, bai_file = run_samtools(
        sam_file,
        config.ALIGNMENTS
    )

logger.stage_end(
    "STAGE 10 : SAMTOOLS"
)

# --------------------------------------------------
# Stage 11 : Mapping Statistics
# --------------------------------------------------

logger.stage_start(
    "STAGE 11 : MAPPING STATISTICS"
)

print(
    "\n========== STAGE 11 : MAPPING STATISTICS ==========\n"
)

for sample in plan:

    sample_id = sample["sample_id"]

    sorted_bam = (
        config.ALIGNMENTS
        / f"{sample_id}.sorted.bam"
    )

    generate_mapping_stats(
        sorted_bam,
        config.MAPPING_STATS
    )

    generate_mapping_summary(
    config.MAPPING_STATS
    )

logger.stage_end(
    "STAGE 11 : MAPPING STATISTICS"
)

# --------------------------------------------------
# Stage 12 : STRINGTIE
# --------------------------------------------------

logger.stage_start(
    "STAGE 12 : STRINGTIE"
)

print(
    "\n========== STAGE 12 : STRINGTIE ==========\n"
)

for sample in plan:

    sample_id = sample["sample_id"]

    sorted_bam = (
        config.ALIGNMENTS
        / f"{sample_id}.sorted.bam"
    )

    run_stringtie(
        sorted_bam,
        GFF,
        config.STRINGTIE
    )

logger.stage_end(
    "STAGE 12 : STRINGTIE"
)

# --------------------------------------------------
# Stage 13 : Generate sample_list.txt
# --------------------------------------------------

logger.stage_start(
    "STAGE 13 : SAMPLE LIST"
)

print(
    "\n========== STAGE 13 : SAMPLE LIST ==========\n"
)

generate_sample_list(
    plan,
    config.STRINGTIE,
    config.SAMPLE_LIST
)

logger.stage_end(
    "STAGE 13 : SAMPLE LIST"
)

# --------------------------------------------------
# Stage 14 : prepDE
# --------------------------------------------------

logger.stage_start(
    "STAGE 14 : PREPDE"
)

print(
    "\n========== STAGE 14 : PREPDE ==========\n"
)

gene_matrix, transcript_matrix = run_prepde(
    config.PREPDE,
    config.SAMPLE_LIST,
    config.COUNTS
)

logger.stage_end(
    "STAGE 14 : PREPDE"
)

# --------------------------------------------------
# Stage 15 : Native edgeR
# --------------------------------------------------

logger.stage_start(
    "STAGE 15 : Native edgeR"
)

print(
    "\n========== STAGE 15 : Native edgeR ==========\n"
)

run_native_edger(
    config.EDGER,
    config.COUNTS / "gene_count_matrix.csv",
    config.METADATA,
    config.RESULTS
)

logger.stage_end(
    "STAGE 15 : Native edgeR"
)

# --------------------------------------------------
# Stage 16 : Trinity Sample File
# --------------------------------------------------

logger.stage_start(
    "STAGE 16 : TRINITY SAMPLE FILE"
)

print(
    "\n========== STAGE 16 : TRINITY SAMPLE FILE ==========\n"
)

create_trinity_sample_file(
    metadata,
    config.TRINITY_SAMPLES
)

trinity_matrix = convert_gene_matrix_to_tsv(
    gene_matrix,
    config.TRINITY_MATRIX
)

logger.stage_end(
    "STAGE 16 : TRINITY SAMPLE FILE"
)

# --------------------------------------------------
# Stage 17 : Trinity edgeR
# --------------------------------------------------

logger.stage_start(
    "STAGE 17 : TRINITY edgeR"
)

print( 
    "\n========== STAGE 17 : TRINITY edgeR ==========\n"
)

run_trinity_edger(
    trinity_matrix,
    config.TRINITY_SAMPLES,
    config.TRINITY_RESULTS
)

logger.stage_end(
    "STAGE 17 : TRINITY edgeR"
)

# --------------------------------------------------
# Stage 18 : PCA
# --------------------------------------------------

logger.stage_start(
    "STAGE 18 : PCA"
)

print(
    "\n========== STAGE 18 : PCA ==========\n"
)

generate_pca_plot(

    config.RESULTS / "normalized_counts.csv",

    config.METADATA,

    config.PLOTS

)

logger.stage_end(
    "STAGE 18 : PCA"
)

# --------------------------------------------------
# Stage 19 : Volcano Plot
# --------------------------------------------------

logger.stage_start(
    "STAGE 19 : VOLCANO PLOT"
)

print(
    "\n========== STAGE 19 : VOLCANO PLOT ==========\n"
)

generate_volcano_plot(

    config.RESULTS / "edger_results.csv",

    config.PLOTS

)

logger.stage_end(
    "STAGE 19 : VOLCANO PLOT"
)

# --------------------------------------------------
# Stage 20 : Heatmap
# --------------------------------------------------

logger.stage_start(
    "STAGE 20 : HEATMAP"
)

print(
    "\n========== STAGE 20 : HEATMAP ==========\n"
)

generate_heatmap(

    config.RESULTS
    / "normalized_counts.csv",
    config.RESULTS / "edger_results.csv",
    config.PLOTS
)

logger.stage_end(
    "STAGE 20 : HEATMAP"
)

# --------------------------------------------------
# Stage 21 : MA Plot
# --------------------------------------------------

logger.stage_start(
    "STAGE 21 : MA PLOT"
)

print(
    "\n========== STAGE 21 : MA PLOT ==========\n"
)

generate_ma_plot(

    config.RESULTS
    / "edger_results.csv",

    config.PLOTS

)

logger.stage_end(
    "STAGE 21 : MA PLOT"
)

# --------------------------------------------------
# Stage 22 : HTML REPORT
# --------------------------------------------------

logger.stage_start(
    "STAGE 22 : HTML REPORT"
)

print(
    "\n========== STAGE 22 : HTML REPORT ==========\n"
)

generate_html_report(

    config.REPORT_TEMPLATE,

    config.MAPPING_STATS / "mapping_summary.csv",

    config.REPORT

)

logger.stage_end(
    "STAGE 22 : HTML REPORT"
)

logger.info("=" * 60)
logger.info("🎉 CHRONOSEQ PIPELINE COMPLETED SUCCESSFULLY 🎉")
logger.info("=" * 60)

logger.runtime_summary()