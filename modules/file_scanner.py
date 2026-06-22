from pathlib import Path


SUPPORTED_EXTENSIONS = {

    ".sra",

}


def find_fastq_files(raw_directory):

    """
    Scan the raw data directory for sequencing files.

    Currently supported:

        • .sra

    Parameters
    ----------

    raw_directory : str or Path

    Returns
    -------

    list[Path]
    """

    raw_directory = Path(raw_directory)

    if not raw_directory.exists():

        raise FileNotFoundError(

            "\n"

            "Raw data directory not found:\n"

            f"{raw_directory}"

        )

    files = sorted(

        [

            file

            for file in raw_directory.iterdir()

            if (

                file.is_file()

                and

                file.suffix.lower()

                in SUPPORTED_EXTENSIONS

            )

        ]

    )

    if not files:

        raise FileNotFoundError(

            "\n"

            "❌ No sequencing files detected.\n\n"

            "Place .sra files inside:\n"

            f"{raw_directory}"

        )

    print()

    print("=" * 60)

    print("RAW DATA DETECTED")

    print("=" * 60)

    for file in files:

        print(f"• {file.name}")

    print("=" * 60)

    return files