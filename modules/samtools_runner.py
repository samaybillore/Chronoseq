import subprocess

from pathlib import Path


def run_samtools(
    sam_file,
    output_directory,
):
    """
    Process SAM file using samtools.

    Steps

    1. SAM -> BAM

    2. Sort BAM

    3. Index BAM

    Returns
    -------

    (bam_file, sorted_bam, bai_file)
    """

    sam_file = Path(sam_file)

    output_directory = Path(output_directory)

    if not sam_file.exists():

        raise FileNotFoundError(

            f"\nSAM file not found:\n{sam_file}"

        )

    output_directory.mkdir(

        parents=True,

        exist_ok=True,

    )

    sample = sam_file.stem

    bam_file = (

        output_directory

        / f"{sample}.bam"

    )

    sorted_bam = (

        output_directory

        / f"{sample}.sorted.bam"

    )

    bai_file = (

        output_directory

        / f"{sample}.sorted.bam.bai"

    )

    # ------------------------------------------
    # Skip if already processed
    # ------------------------------------------

    if (

        sorted_bam.exists()

        and

        bai_file.exists()

    ):

        print(

            f"✅ Samtools already completed: "

            f"{sample}"

        )

        return (

            bam_file,

            sorted_bam,

            bai_file,

        )

    print()

    print("=" * 60)

    print(

        f"Running Samtools : {sample}"

    )

    print("=" * 60)

    # ------------------------------------------
    # SAM -> BAM
    # ------------------------------------------

    subprocess.run(

        [

            "samtools",

            "view",

            "-bS",

            "-o",

            str(bam_file),

            str(sam_file),

        ],

        check=True,

    )

    # ------------------------------------------
    # Sort
    # ------------------------------------------

    subprocess.run(

        [

            "samtools",

            "sort",

            "-o",

            str(sorted_bam),

            str(bam_file),

        ],

        check=True,

    )

    # ------------------------------------------
    # Index
    # ------------------------------------------

    subprocess.run(

        [

            "samtools",

            "index",

            str(sorted_bam),

        ],

        check=True,

    )

    if not sorted_bam.exists():

        raise RuntimeError(

            f"Samtools failed for "

            f"{sample}"

        )

    if not bai_file.exists():

        raise RuntimeError(

            f"BAM indexing failed for "

            f"{sample}"

        )

    print(

        f"✅ Samtools completed: "

        f"{sample}"

    )

    return (

        bam_file,

        sorted_bam,

        bai_file,

    )