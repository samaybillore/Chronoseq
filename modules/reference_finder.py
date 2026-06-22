from pathlib import Path


FASTA_EXTENSIONS = {

    ".fa",

    ".fasta",

    ".fna",

}


GFF_EXTENSIONS = {

    ".gff",

    ".gff3",

    ".gtf",

}


def find_reference_files(reference_directory):

    """
    Automatically detect the reference genome
    and annotation file.

    Parameters
    ----------

    reference_directory : str or Path

    Returns
    -------

    tuple

        (fasta_file, annotation_file)
    """

    reference_directory = Path(reference_directory)

    if not reference_directory.exists():

        raise FileNotFoundError(

            "\n"

            "Reference directory not found:\n"

            f"{reference_directory}"

        )

    fasta_files = [

        file

        for file in reference_directory.iterdir()

        if (

            file.is_file()

            and

            file.suffix.lower()

            in FASTA_EXTENSIONS

        )

    ]

    annotation_files = [

        file

        for file in reference_directory.iterdir()

        if (

            file.is_file()

            and

            file.suffix.lower()

            in GFF_EXTENSIONS

        )

    ]

    # ------------------------------------------
    # FASTA validation
    # ------------------------------------------

    if len(fasta_files) == 0:

        raise FileNotFoundError(

            "\n"

            "❌ No reference genome found.\n\n"

            "Place exactly one file with extension:\n"

            ".fa / .fasta / .fna\n\n"

            f"in:\n{reference_directory}"

        )

    if len(fasta_files) > 1:

        files = "\n".join(

            f"  • {x.name}"

            for x in fasta_files

        )

        raise ValueError(

            "\n"

            "❌ Multiple FASTA files detected.\n\n"

            f"{files}\n\n"

            "Keep only one reference genome."

        )

    # ------------------------------------------
    # Annotation validation
    # ------------------------------------------

    if len(annotation_files) == 0:

        raise FileNotFoundError(

            "\n"

            "❌ No annotation file found.\n\n"

            "Place exactly one file with extension:\n"

            ".gff / .gff3 / .gtf\n\n"

            f"in:\n{reference_directory}"

        )

    if len(annotation_files) > 1:

        files = "\n".join(

            f"  • {x.name}"

            for x in annotation_files

        )

        raise ValueError(

            "\n"

            "❌ Multiple annotation files detected.\n\n"

            f"{files}\n\n"

            "Keep only one annotation file."

        )

    fasta = fasta_files[0]

    annotation = annotation_files[0]

    print()

    print("=" * 60)

    print("REFERENCE FILES DETECTED")

    print("=" * 60)

    print(f"Genome     : {fasta.name}")

    print(f"Annotation : {annotation.name}")

    print("=" * 60)

    return fasta, annotation