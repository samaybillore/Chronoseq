import subprocess
from pathlib import Path


def run_native_edger(
    r_script,
    count_matrix,
    metadata,
    output_directory,
):
    """
    Run edgeR differential expression analysis.

    Parameters
    ----------
    r_script : str or Path

    count_matrix : str or Path

    metadata : str or Path

    output_directory : str or Path

    Returns
    -------
    Path

        edgeR results CSV.
    """

    r_script = Path(r_script)

    count_matrix = Path(count_matrix)

    metadata = Path(metadata)

    output_directory = Path(output_directory)

    if not r_script.exists():

        raise FileNotFoundError(

            f"\nR script not found:\n{r_script}"

        )

    if not count_matrix.exists():

        raise FileNotFoundError(

            f"\nCount matrix not found:\n{count_matrix}"

        )

    if not metadata.exists():

        raise FileNotFoundError(

            f"\nMetadata file not found:\n{metadata}"

        )

    output_directory.mkdir(

        parents=True,

        exist_ok=True,

    )

    results_file = (

        output_directory

        / "edgeR_results.csv"

    )

    # ------------------------------------------
    # Skip completed analysis
    # ------------------------------------------

    if results_file.exists():

        print()

        print("=" * 60)

        print("edgeR analysis already completed.")

        print("=" * 60)

        return results_file

    print()

    print("=" * 60)

    print("Running edgeR Analysis")

    print("=" * 60)

    subprocess.run(

        [

            "Rscript",

            str(r_script),

            str(count_matrix),

            str(metadata),

            str(results_file),

        ],

        check=True,

    )

    if not results_file.exists():

        raise RuntimeError(

            "edgeR output file was not generated."

        )

    print(

        "✅ edgeR analysis completed."

    )

    return results_file