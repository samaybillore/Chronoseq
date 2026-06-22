from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_ma_plot(

    edger_results,

    output_file,

    logfc_column="logFC",

    logcpm_column="logCPM",

    pvalue_column="PValue",

):
    """
    Generate MA plot from edgeR results.

    Parameters
    ----------
    edger_results : str or Path

    output_file : str or Path
    """

    edger_results = Path(edger_results)

    output_file = Path(output_file)

    if not edger_results.exists():

        raise FileNotFoundError(

            f"\nedgeR results not found:\n"

            f"{edger_results}"

        )

    df = pd.read_csv(

        edger_results

    )

    required = [

        logfc_column,

        logcpm_column,

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

    significant = (

        (df[pvalue_column] < 0.05)

        &

        (abs(df[logfc_column]) >= 1)

    )

    plt.figure(

        figsize=(8, 6)

    )

    plt.scatter(

        df.loc[~significant, logcpm_column],

        df.loc[~significant, logfc_column],

        s=10,

        alpha=0.5,

        label="Not Significant",

    )

    plt.scatter(

        df.loc[significant, logcpm_column],

        df.loc[significant, logfc_column],

        s=12,

        alpha=0.8,

        label="Significant",

    )

    plt.axhline(

        1,

        linestyle="--",

        linewidth=1,

    )

    plt.axhline(

        -1,

        linestyle="--",

        linewidth=1,

    )

    plt.xlabel(

        "Average Expression (logCPM)"

    )

    plt.ylabel(

        "log2 Fold Change"

    )

    plt.title(

        "MA Plot"

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

        f"✅ MA plot generated:\n"

        f"{output_file}"

    )

    return output_file