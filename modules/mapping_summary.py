from pathlib import Path

import pandas as pd


def generate_mapping_summary(

    mapping_stats_directory,

    output_csv,

):
    """
    Create a mapping summary table from
    samtools flagstat outputs.

    Returns
    -------
    pandas.DataFrame
    """

    mapping_stats_directory = Path(

        mapping_stats_directory

    )

    output_csv = Path(output_csv)

    if not mapping_stats_directory.exists():

        raise FileNotFoundError(

            f"\nDirectory not found:\n"

            f"{mapping_stats_directory}"

        )

    records = []

    for stats_file in sorted(

        mapping_stats_directory.glob(

            "*_mapping_stats.txt"

        )

    ):

        sample = stats_file.name.replace(

            "_mapping_stats.txt",

            ""

        )

        total = None

        mapped = None

        with open(

            stats_file,

            "r",

            encoding="utf-8",

        ) as f:

            lines = f.readlines()

        if len(lines) > 0:

            total = int(

                lines[0].split()[0]

            )

        if len(lines) > 4:

            mapped = int(

                lines[4].split()[0]

            )

        if (

            total is None

            or

            mapped is None

        ):

            continue

        percentage = (

            mapped

            / total

            * 100

        )

        records.append(

            {

                "Sample": sample,

                "Total Reads": total,

                "Mapped Reads": mapped,

                "Mapping Rate (%)": round(

                    percentage,

                    2,

                ),

            }

        )

    df = pd.DataFrame(

        records

    )

    output_csv.parent.mkdir(

        parents=True,

        exist_ok=True,

    )

    df.to_csv(

        output_csv,

        index=False,

    )

    print()

    print("=" * 60)

    print(

        "Mapping summary generated."

    )

    print(

        f"Samples : {len(df)}"

    )

    print(

        f"Output  : {output_csv}"

    )

    print("=" * 60)

    print()

    return df