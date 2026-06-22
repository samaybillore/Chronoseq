import subprocess
from pathlib import Path
import os


def run_fastqc(fastq_file, output_directory):
    """
    Run FastQC on a FASTQ file.

    Parameters
    ----------
    fastq_file : str or Path

    output_directory : str or Path

    Returns
    -------
    Path

        Path to generated HTML report.
    """

    fastq_file = Path(fastq_file)

    output_directory = Path(output_directory)

    if not fastq_file.exists():

        raise FileNotFoundError(

            f"\nFASTQ file not found:\n{fastq_file}"

        )

    output_directory.mkdir(

        parents=True,

        exist_ok=True

    )

    report = (

        output_directory

        / f"{fastq_file.stem}_fastqc.html"

    )

    # --------------------------------------------------
    # Skip existing reports
    # --------------------------------------------------

    if report.exists():

        print(

            f"✅ FastQC already completed: "

            f"{fastq_file.name}"

        )

        return report

    print(

        f"Running FastQC on "

        f"{fastq_file.name}"

    )

    subprocess.run(

        [

            "fastqc",

            "--threads",

            str(os.cpu_count()),

            "-o",

            str(output_directory),

            str(fastq_file),

        ],

        check=True,

    )

    if not report.exists():

        raise RuntimeError(

            f"FastQC failed for "

            f"{fastq_file.name}"

        )

    print(

        f"✅ FastQC completed: "

        f"{fastq_file.name}"

    )

    return report