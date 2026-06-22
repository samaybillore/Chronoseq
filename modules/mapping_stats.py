from pathlib import Path
import subprocess


def generate_mapping_stats(
    sorted_bam,
    output_directory,
):
    """
    Generate mapping statistics using
    samtools flagstat.

    Parameters
    ----------
    sorted_bam : str or Path

    output_directory : str or Path

    Returns
    -------
    Path

        Path to mapping statistics file.
    """

    sorted_bam = Path(sorted_bam)

    output_directory = Path(output_directory)

    if not sorted_bam.exists():

        raise FileNotFoundError(

            f"\nSorted BAM not found:\n"

            f"{sorted_bam}"

        )

    output_directory.mkdir(

        parents=True,

        exist_ok=True,

    )

    sample = sorted_bam.stem.replace(

        ".sorted",

        ""

    )

    stats_file = (

        output_directory

        / f"{sample}_mapping_stats.txt"

    )

    # ------------------------------------------
    # Skip existing output
    # ------------------------------------------

    if stats_file.exists():

        print(

            f"✅ Mapping statistics already exist: "

            f"{sample}"

        )

        return stats_file

    print()

    print("=" * 60)

    print(

        f"Generating mapping statistics: "

        f"{sample}"

    )

    print("=" * 60)

    with open(

        stats_file,

        "w",

        encoding="utf-8",

    ) as outfile:

        subprocess.run(

            [

                "samtools",

                "flagstat",

                str(sorted_bam),

            ],

            stdout=outfile,

            check=True,

        )

    if not stats_file.exists():

        raise RuntimeError(

            f"Failed to generate mapping statistics "

            f"for {sample}"

        )

    print(

        f"✅ Mapping statistics generated: "

        f"{sample}"

    )

    return stats_file