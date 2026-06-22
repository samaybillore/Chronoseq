import subprocess
from pathlib import Path


def run_trimmomatic(

    fastq_1,

    fastq_2,

    output_directory,

    adapters,

    threads=4,

):
    """
    Run Trimmomatic on paired-end FASTQ files.

    Parameters
    ----------
    fastq_1 : str or Path

    fastq_2 : str or Path

    output_directory : str or Path

    adapters : str or Path

    threads : int

    Returns
    -------
    tuple

        (
            paired_1,
            unpaired_1,
            paired_2,
            unpaired_2
        )
    """

    fastq_1 = Path(fastq_1)
    fastq_2 = Path(fastq_2)

    output_directory = Path(output_directory)

    adapters = Path(adapters)

    if not fastq_1.exists():

        raise FileNotFoundError(

            f"\nFASTQ not found:\n{fastq_1}"

        )

    if not fastq_2.exists():

        raise FileNotFoundError(

            f"\nFASTQ not found:\n{fastq_2}"

        )

    if not adapters.exists():

        raise FileNotFoundError(

            f"\nAdapter file not found:\n{adapters}"

        )

    output_directory.mkdir(

        parents=True,

        exist_ok=True

    )

    sample = (

        fastq_1.name

        .replace("_1.fastq", "")

        .replace(".fastq", "")

    )

    paired_1 = (

        output_directory

        / f"{sample}_1_paired.fq.gz"

    )

    unpaired_1 = (

        output_directory

        / f"{sample}_1_unpaired.fq.gz"

    )

    paired_2 = (

        output_directory

        / f"{sample}_2_paired.fq.gz"

    )

    unpaired_2 = (

        output_directory

        / f"{sample}_2_unpaired.fq.gz"

    )

    # --------------------------------------------------
    # Skip completed samples
    # --------------------------------------------------

    if (

        paired_1.exists()

        and

        paired_2.exists()

    ):

        print(

            f"✅ Trimming already completed: "

            f"{sample}"

        )

        return (

            paired_1,

            unpaired_1,

            paired_2,

            unpaired_2,

        )

    print()

    print("=" * 60)

    print(

        f"Running Trimmomatic : {sample}"

    )

    print("=" * 60)

    subprocess.run(

        [

            "trimmomatic",

            "PE",

            "-threads",

            str(threads),

            str(fastq_1),

            str(fastq_2),

            str(paired_1),

            str(unpaired_1),

            str(paired_2),

            str(unpaired_2),

            f"ILLUMINACLIP:{adapters}:2:30:10",

            "LEADING:3",

            "TRAILING:3",

            "SLIDINGWINDOW:4:15",

            "MINLEN:36",

        ],

        check=True,

    )

    if not paired_1.exists():

        raise RuntimeError(

            f"Trimmomatic failed for "

            f"{sample}"

        )

    print(

        f"✅ Trimmomatic completed: "

        f"{sample}"

    )

    return (

        paired_1,

        unpaired_1,

        paired_2,

        unpaired_2,

    )