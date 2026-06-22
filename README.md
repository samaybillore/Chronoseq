# 🧬 CHRONOSEQ

> **CHRONOSEQ (Systematic RNA-seq Analysis Pipeline)** is an automated, modular, reproducible, and user-friendly RNA-seq differential gene expression analysis pipeline developed in Python. It streamlines the complete workflow from raw sequencing data to publication-ready results with minimal user intervention.

---

# ✨ Features

* 📥 Automatic SRA to FASTQ conversion
* 🔍 FastQC quality assessment
* 📊 MultiQC report generation
* ✂️ Adapter and quality trimming using Trimmomatic
* 🧬 Bowtie2 genome indexing and alignment
* 📁 SAM/BAM processing with SAMtools
* 📈 Mapping statistics generation
* 🧾 Transcript quantification using StringTie
* 🔢 Gene count matrix generation using `prepDE.py3`
* 📊 Differential expression analysis using:

  * Native edgeR
  * Trinity edgeR
* 📉 PCA visualization
* 🌋 Volcano plot generation
* 🔥 Heatmap generation
* 📈 MA plot generation
* 📄 Automated HTML report generation
* 📝 Integrated logging and runtime summaries
* ⚙️ Automatic dependency checking and optional installation

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/<YOUR_USERNAME>/chronoseq.git

cd CHRONOSEQ
```

Create the Conda environment:

```bash
conda env create -f environment.yml

conda activate CHRONOSEQ
```

---

# 📂 Metadata Format

`metadata.csv`

```csv
sample_id,condition,replicate

SRR000001,Control,1
SRR000002,Control,2
SRR000003,Treated,1
SRR000004,Treated,2
```

The `condition` column is generic and supports any comparison, including:

* Control vs Treated
* WT vs Knockout
* Tumor vs Normal
* Disease vs Healthy
* Resistant vs Sensitive
* Any custom biological condition

---

# 📁 Reference Files

Place exactly one reference genome and one annotation file in:

```
data/reference/
```

Supported genome formats:

* `.fa`
* `.fasta`
* `.fna`

Supported annotation formats:

* `.gff`
* `.gff3`
* `.gtf`

CHRONOSEQ automatically detects the files without requiring predefined filenames.

---

# ▶️ Running CHRONOSEQ

```bash
python main.py
```

During startup, CHRONOSEQ automatically validates:

* Python version
* Python dependencies
* Java installation
* Bioinformatics tools
* R installation
* R packages
* Project directories
* Metadata template
* Adapter resources

If supported dependencies are missing, CHRONOSEQ can optionally install them after user confirmation.

---

# 📊 Pipeline Overview

```
SRA
 │
 ▼
FASTQ
 │
 ▼
FastQC
 │
 ▼
MultiQC
 │
 ▼
Trimmomatic
 │
 ▼
FastQC
 │
 ▼
MultiQC
 │
 ▼
Bowtie2
 │
 ▼
SAMtools
 │
 ▼
Mapping Statistics
 │
 ▼
StringTie
 │
 ▼
prepDE.py3
 │
 ├──────────────► Native edgeR
 │
 └──────────────► Trinity edgeR
                     │
                     ▼
      PCA • Volcano • Heatmap • MA Plot
                     │
                     ▼
              HTML Final Report
```

---

# 📂 Output Files

CHRONOSEQ automatically generates:

* Quality control reports
* MultiQC summaries
* Trimmed reads
* Genome alignments
* Sorted BAM files
* BAM indexes
* Mapping statistics
* Count matrices
* Differential expression results
* PCA plots
* Volcano plots
* Heatmaps
* MA plots
* HTML summary reports
* Runtime logs

---

# 🛠 Technologies

* Python
* FastQC
* MultiQC
* Trimmomatic
* Bowtie2
* SAMtools
* StringTie
* edgeR
* Trinity
* R
* Pandas
* NumPy
* Matplotlib
* SciPy
* scikit-learn

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

**Samay Billore**

Bachelor of Science in Biotechnology

Interests:

* Bioinformatics
* Genomics
* RNA-seq Analysis
* Next-Generation Sequencing
* Computational Biology

---

# 🤝 Contributing

Contributions, suggestions, feature requests, and bug reports are welcome.

Feel free to fork the repository and submit a pull request.

---

# ⭐ Citation

If CHRONOSEQ contributes to your research, please cite the GitHub repository and acknowledge the project in your publication.

---

# 🚧 Roadmap

Future planned features include:

* Snakemake backend
* Nextflow support
* Docker container
* Interactive web interface
* Automated functional enrichment analysis
* KEGG and GO analysis
* Batch effect correction
* Multi-thread optimization
* Cloud execution support
