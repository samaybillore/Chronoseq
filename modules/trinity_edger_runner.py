from pathlib import Path
import subprocess


def run_trinity_edger(
    matrix_file,
    samples_file,
    output_directory,
):
    """
    Run Trinity Differential Expression Analysis
    using edgeR.

    Parameters
    ----------
    matrix_file : str or Path
        Trinity-compatible gene count matrix (.tsv)

    samples_file : str or Path
        Trinity samples.txt file

    output_directory : str or Path
        Directory where Trinity outputs will be written

    Returns
    -------
    Path
        Output directory containing Trinity DE results.
    """

    matrix_file = Path(matrix_file)
    samples_file = Path(samples_file)
    output_directory = Path(output_directory)

    if not matrix_file.exists():

        raise FileNotFoundError(

            f"\nMatrix file not found:\n"

            f"{matrix_file}"

        )

    if not samples_file.exists():

        raise FileNotFoundError(

            f"\nSamples file not found:\n"

            f"{samples_file}"

        )

    output_directory.mkdir(

        parents=True,

        exist_ok=True,

    )

    # --------------------------------------------------
    # Skip if already completed
    # --------------------------------------------------

    if any(output_directory.iterdir()):

        print()

        print("=" * 60)

        print("✅ Trinity edgeR results already exist.")

        print("=" * 60)

        return output_directory

    print()

    print("=" * 60)

    print("Running Trinity Differential Expression (edgeR)")

    print("=" * 60)

    subprocess.run(

        [

            "run_DE_analysis.pl",

            "--matrix",

            str(matrix_file),

            "--method",

            "edgeR",

            "--samples_file",

            str(samples_file),

        ],

        cwd=output_directory,

        check=True,

    )

    print()

    print("=" * 60)

    print("✅ Trinity edgeR completed successfully.")

    print("=" * 60)

    return output_directory