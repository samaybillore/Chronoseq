import os
import subprocess

from pathlib import Path


def run_stringtie(

    sorted_bam,

    annotation,

    output_directory,

    threads=None,

):
    """
    Run StringTie transcript quantification.

    Parameters
    ----------
    sorted_bam : str or Path

    annotation : str or Path

    output_directory : str or Path

    Returns
    -------
    Path

        Generated GTF file.
    """

    sorted_bam = Path(sorted_bam)

    annotation = Path(annotation)

    output_directory = Path(output_directory)

    if threads is None:

        threads = os.cpu_count()

    if not sorted_bam.exists():

        raise FileNotFoundError(

            f"\nSorted BAM not found:\n"

            f"{sorted_bam}"

        )

    if not annotation.exists():

        raise FileNotFoundError(

            f"\nAnnotation file not found:\n"

            f"{annotation}"

        )

    output_directory.mkdir(

        parents=True,

        exist_ok=True,

    )

    sample = sorted_bam.stem.replace(

        ".sorted",

        ""

    )

    gtf_file = (

        output_directory

        / f"{sample}.gtf"

    )

    # ------------------------------------------
    # Skip existing output
    # ------------------------------------------

    if gtf_file.exists():

        print(

            f"✅ StringTie already completed: "

            f"{sample}"

        )

        return gtf_file

    print()

    print("=" * 60)

    print(

        f"Running StringTie : {sample}"

    )

    print("=" * 60)

    subprocess.run(

        [

            "stringtie",

            str(sorted_bam),

            "-G",

            str(annotation),

            "-o",

            str(gtf_file),

            "-p",

            str(threads),

            "-e",

            "-B",

        ],

        check=True,

    )

    if not gtf_file.exists():

        raise RuntimeError(

            f"StringTie failed for "

            f"{sample}"

        )

    print(

        f"✅ StringTie completed: "

        f"{sample}"

    )

    return gtf_file