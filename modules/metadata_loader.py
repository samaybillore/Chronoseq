from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [

    "sample_id",

    "condition",

    "replicate",

]


def load_metadata(csv_path):

    """
    Load and validate metadata.

    Required columns:

        sample_id

        condition

        replicate

    Returns
    -------

    pandas.DataFrame

    """

    csv_path = Path(csv_path)

    if not csv_path.exists():

        raise FileNotFoundError(

            f"\nMetadata file not found:\n{csv_path}"

        )

    df = pd.read_csv(csv_path)

    # --------------------------------------------------
    # Check required columns
    # --------------------------------------------------

    missing = [

        column

        for column in REQUIRED_COLUMNS

        if column not in df.columns

    ]

    if missing:

        raise ValueError(

            "\nmetadata.csv is missing required column(s):\n\n"

            + "\n".join(missing)

        )

    # --------------------------------------------------
    # Keep only required columns
    # --------------------------------------------------

    df = df[REQUIRED_COLUMNS]

    # --------------------------------------------------
    # Remove whitespace
    # --------------------------------------------------

    df["sample_id"] = (

        df["sample_id"]

        .astype(str)

        .str.strip()

    )

    df["condition"] = (

        df["condition"]

        .astype(str)

        .str.strip()

    )

    # --------------------------------------------------
    # Missing values
    # --------------------------------------------------

    if df.isnull().values.any():

        raise ValueError(

            "\nmetadata.csv contains missing values."

        )

    # --------------------------------------------------
    # Duplicate sample IDs
    # --------------------------------------------------

    duplicates = df[

        df["sample_id"].duplicated()

    ]

    if not duplicates.empty:

        raise ValueError(

            "\nDuplicate sample_id(s) found:\n\n"

            + "\n".join(

                duplicates["sample_id"]

            )

        )

    # --------------------------------------------------
    # Replicate validation
    # --------------------------------------------------

    try:

        df["replicate"] = (

            df["replicate"]

            .astype(int)

        )

    except Exception:

        raise ValueError(

            "\nReplicate column must contain integers."

        )

    # --------------------------------------------------
    # Minimum samples
    # --------------------------------------------------

    if len(df) < 2:

        raise ValueError(

            "\nAt least two samples are required."

        )

    return df