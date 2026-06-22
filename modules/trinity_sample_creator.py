from pathlib import Path

import pandas as pd


def create_trinity_sample_file(
    metadata_file,
    output_file,
):
    """
    Create Trinity samples.txt file.

    Format:

    condition    replicate    sample_id
    """

    metadata_file = Path(metadata_file)

    output_file = Path(output_file)

    if not metadata_file.exists():

        raise FileNotFoundError(

            f"\nMetadata not found:\n{metadata_file}"

        )

    df = pd.read_csv(metadata_file)

    required = [

        "sample_id",

        "condition",

        "replicate",

    ]

    missing = [

        x

        for x in required

        if x not in df.columns

    ]

    if missing:

        raise ValueError(

            f"Missing columns: {missing}"

        )

    output_file.parent.mkdir(

        parents=True,

        exist_ok=True,

    )

    with open(

        output_file,

        "w",

        encoding="utf-8",

    ) as f:

        f.write(

            "condition\treplicate\tsample_id\n"

        )

        for _, row in df.iterrows():

            f.write(

                f"{row['condition']}\t"

                f"{row['replicate']}\t"

                f"{row['sample_id']}\n"

            )

    print(

        f"✅ Trinity samples file created:\n"

        f"{output_file}"

    )

    return output_file