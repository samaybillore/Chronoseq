from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def generate_volcano_plot(

    edger_results,

    output_file,

    logfc_column="logFC",

    pvalue_column="PValue",

    gene_column=None,

):
    """
    Generate a publication-quality volcano plot.

    Parameters
    ----------
    edger_results : str or Path

    output_file : str or Path

    logfc_column : str

    pvalue_column : str

    gene_column : str or None
    """

    edger_results = Path(edger_results)

    output_file = Path(output_file)

    if not edger_results.exists():

        raise FileNotFoundError(

            f"\nedgeR results not found:\n"

            f"{edger_results}"

        )

    df = pd.read_csv(edger_results)

    required = [

        logfc_column,

        pvalue_column,

    ]

    missing = [

        x

        for x in required

        if x not in df.columns

    ]

    if missing:

        raise ValueError(

            f"Missing required columns: {missing}"

        )

    df["neg_log10_p"] = (

        -np.log10(

            df[pvalue_column]

        )

    )

    significant = (

        (df[pvalue_column] < 0.05)

        &

        (abs(df[logfc_column]) >= 1)

    )

    plt.figure(

        figsize=(8, 6)

    )

    plt.scatter(

        df.loc[~significant, logfc_column],

        df.loc[~significant, "neg_log10_p"],

        s=10,

        alpha=0.5,

        label="Not Significant",

    )

    plt.scatter(

        df.loc[significant, logfc_column],

        df.loc[significant, "neg_log10_p"],

        s=12,

        alpha=0.8,

        label="Significant",

    )

    plt.axhline(

        -np.log10(0.05),

        linestyle="--",

        linewidth=1,

    )

    plt.axvline(

        1,

        linestyle="--",

        linewidth=1,

    )

    plt.axvline(

        -1,

        linestyle="--",

        linewidth=1,

    )

    # ----------------------------------------
    # Label top genes
    # ----------------------------------------

    if (

        gene_column is not None

        and

        gene_column in df.columns

    ):

        top = df.nsmallest(

            10,

            pvalue_column,

        )

        for _, row in top.iterrows():

            plt.text(

                row[logfc_column],

                row["neg_log10_p"],

                str(

                    row[gene_column]

                ),

                fontsize=7,

            )

    plt.xlabel(

        "log2 Fold Change"

    )

    plt.ylabel(

        "-log10(P-value)"

    )

    plt.title(

        "Volcano Plot"

    )

    plt.legend()

    plt.tight_layout()

    output_file.parent.mkdir(

        parents=True,

        exist_ok=True,

    )

    plt.savefig(

        output_file,

        dpi=300,

    )

    plt.close()

    print(

        f"✅ Volcano plot generated:\n"

        f"{output_file}"

    )

    return output_file