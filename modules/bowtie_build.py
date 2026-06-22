import subprocess
from pathlib import Path


def build_bowtie2_index(reference_fasta, index_prefix):
    """
    Build a Bowtie2 index.

    Parameters
    ----------
    reference_fasta : str or Path

    index_prefix : str or Path

    Returns
    -------
    Path

        Bowtie2 index prefix.
    """

    reference_fasta = Path(reference_fasta)

    index_prefix = Path(index_prefix)

    if not reference_fasta.exists():

        raise FileNotFoundError(

            f"\nReference genome not found:\n"

            f"{reference_fasta}"

        )

    index_prefix.parent.mkdir(

        parents=True,

        exist_ok=True

    )

    expected_index = (

        index_prefix.parent

        / f"{index_prefix.name}.1.bt2"

    )

    # --------------------------------------------------
    # Skip existing index
    # --------------------------------------------------

    if expected_index.exists():

        print()

        print("=" * 60)

        print("Bowtie2 index already exists.")

        print("=" * 60)

        return index_prefix

    print()

    print("=" * 60)

    print("Building Bowtie2 Index")

    print("=" * 60)

    subprocess.run(

        [

            "bowtie2-build",

            str(reference_fasta),

            str(index_prefix),

        ],

        check=True,

    )

    if not expected_index.exists():

        raise RuntimeError(

            "Bowtie2 index generation failed."

        )

    print(

        "✅ Bowtie2 index created successfully."

    )

    return index_prefix