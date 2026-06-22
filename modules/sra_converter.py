import subprocess
from pathlib import Path


def convert_sra_to_fastq(sra_file, output_directory):
    """
    Convert an SRA file to paired-end FASTQ files using fasterq-dump.
    """

    sra_file = Path(sra_file)
    output_directory = Path(output_directory)

    if not sra_file.exists():

        raise FileNotFoundError(

            f"SRA file not found:\n{sra_file}"

        )

    output_directory.mkdir(

        parents=True,

        exist_ok=True

    )

    sample = sra_file.stem

    fastq_1 = output_directory / f"{sample}_1.fastq"
    fastq_2 = output_directory / f"{sample}_2.fastq"

    # --------------------------------------------------
    # Skip if already converted
    # --------------------------------------------------

    if fastq_1.exists() and fastq_2.exists():

        print(

            f"✅ FASTQ already exists for {sample}"

        )

        return fastq_1, fastq_2

    print()

    print("=" * 60)
    print(f"Converting {sample}")
    print("=" * 60)

    command = [

        "fasterq-dump",

        "--split-files",

        "-O",

        str(output_directory),

        str(sra_file)

    ]

    subprocess.run(

        command,

        check=True

    )

    if not fastq_1.exists():

        raise RuntimeError(

            f"FASTQ conversion failed for {sample}"

        )

    print(

        f"✅ Conversion completed: {sample}"

    )

    return fastq_1, fastq_2