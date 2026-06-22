import subprocess

from pathlib import Path


def run_multiqc(input_directory, output_directory):
    """
    Generate a MultiQC report.

    Parameters
    ----------
    input_directory : str or Path

    output_directory : str or Path

    Returns
    -------
    Path

        Generated HTML report.
    """

    input_directory = Path(input_directory)

    output_directory = Path(output_directory)

    if not input_directory.exists():

        raise FileNotFoundError(

            f"\nInput directory not found:\n"

            f"{input_directory}"

        )

    output_directory.mkdir(

        parents=True,

        exist_ok=True

    )

    report = (

        output_directory

        / "multiqc_report.html"

    )

    # ------------------------------------------
    # Skip existing report
    # ------------------------------------------

    if report.exists():

        print(

            "✅ MultiQC report already exists."

        )

        return report

    print()

    print("=" * 60)

    print("Generating MultiQC Report")

    print("=" * 60)

    subprocess.run(

        [

            "multiqc",

            str(input_directory),

            "-o",

            str(output_directory),

            "-f",

        ],

        check=True,

    )

    if not report.exists():

        raise RuntimeError(

            "MultiQC report generation failed."

        )

    print(

        "✅ MultiQC report generated."

    )

    return report