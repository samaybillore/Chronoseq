from pathlib import Path

import pandas as pd


def convert_gene_matrix_to_tsv(
    csv_file,
    tsv_file,
):
    """
    Convert prepDE CSV matrix
    to Trinity-compatible TSV.
    """

    csv_file = Path(csv_file)

    tsv_file = Path(tsv_file)

    if not csv_file.exists():

        raise FileNotFoundError(

            f"\nMatrix not found:\n{csv_file}"

        )

    df = pd.read_csv(

        csv_file,

        index_col=0,

    )

    tsv_file.parent.mkdir(

        parents=True,

        exist_ok=True,

    )

    df.to_csv(

        tsv_file,

        sep="\t",

    )

    print(

        f"✅ Trinity matrix created:\n"

        f"{tsv_file}"

    )

    return tsv_file