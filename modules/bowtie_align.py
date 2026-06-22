import os
import subprocess

from pathlib import Path


def run_bowtie_align(

    fastq_1,

    fastq_2,

    index_prefix,

    output_directory,

    threads=None,

):
    """
    Run Bowtie2 paired-end alignment.
    """

    fastq_1 = Path(fastq_1)

    fastq_2 = Path(fastq_2)

    index_prefix = Path(index_prefix)

    output_directory = Path(output_directory)

    if threads is None:

        threads = os.cpu_count()

    if not fastq_1.exists():

        raise FileNotFoundError(

            f"\nFASTQ not found:\n{fastq_1}"

        )

    if not fastq_2.exists():

        raise FileNotFoundError(

            f"\nFASTQ not found:\n{fastq_2}"

        )

    if not (

        Path(

            str(index_prefix) + ".1.bt2"

        ).exists()

    ):

        raise FileNotFoundError(

            "\nBowtie2 index not found."

        )

    output_directory.mkdir(

        parents=True,

        exist_ok=True

    )

    sample = (

        fastq_1.name

        .replace("_1_paired.fq.gz", "")

        .replace("_1.fastq", "")

        .replace(".fastq", "")

    )

    sam_file = (

        output_directory

        / f"{sample}.sam"

    )

    # ------------------------------------------
    # Skip completed alignment
    # ------------------------------------------

    if sam_file.exists():

        print(

            f"✅ Alignment already exists: "

            f"{sample}"

        )

        return sam_file

    print()

    print("=" * 60)

    print(

        f"Running Bowtie2 : {sample}"

    )

    print("=" * 60)

    subprocess.run(

        [

            "bowtie2",

            "-x",

            str(index_prefix),

            "-1",

            str(fastq_1),

            "-2",

            str(fastq_2),

            "-S",

            str(sam_file),

            "-p",

            str(threads),

        ],

        check=True,

    )

    if not sam_file.exists():

        raise RuntimeError(

            f"Bowtie2 failed for "

            f"{sample}"

        )

    print(

        f"✅ Alignment completed: "

        f"{sample}"

    )

    return sam_file