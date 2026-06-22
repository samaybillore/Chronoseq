import subprocess
from pathlib import Path


def run_prepde(
    prepde_script,
    sample_list,
    output_directory,
):
    """
    Run StringTie prepDE.py3 to generate
    gene and transcript count matrices.

    Parameters
    ----------
    prepde_script : str or Path

    sample_list : str or Path

    output_directory : str or Path

    Returns
    -------
    tuple

        (
            gene_count_matrix,
            transcript_count_matrix
        )
    """

    prepde_script = Path(prepde_script)

    sample_list = Path(sample_list)

    output_directory = Path(output_directory)

    if not prepde_script.exists():

        raise FileNotFoundError(

            f"\nprepDE.py3 not found:\n"

            f"{prepde_script}"

        )

    if not sample_list.exists():

        raise FileNotFoundError(

            f"\nSample list not found:\n"

            f"{sample_list}"

        )

    output_directory.mkdir(

        parents=True,

        exist_ok=True,

    )

    gene_matrix = (

        output_directory

        / "gene_count_matrix.csv"

    )

    transcript_matrix = (

        output_directory

        / "transcript_count_matrix.csv"

    )

    # ------------------------------------------
    # Skip existing matrices
    # ------------------------------------------

    if (

        gene_matrix.exists()

        and

        transcript_matrix.exists()

    ):

        print()

        print("=" * 60)

        print("prepDE already completed.")

        print("=" * 60)

        return (

            gene_matrix,

            transcript_matrix,

        )

    print()

    print("=" * 60)

    print("Running prepDE.py3")

    print("=" * 60)

    subprocess.run(

        [

            "python3",

            str(prepde_script),

            "-i",

            str(sample_list),

            "-g",

            str(gene_matrix),

            "-t",

            str(transcript_matrix),

        ],

        check=True,

        cwd=output_directory,

    )

    if not gene_matrix.exists():

        raise RuntimeError(

            "Gene count matrix was not generated."

        )

    if not transcript_matrix.exists():

        raise RuntimeError(

            "Transcript count matrix was not generated."

        )

    print("✅ prepDE completed successfully.")

    return (

        gene_matrix,

        transcript_matrix,

    )