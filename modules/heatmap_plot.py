from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_heatmap(

    count_matrix,

    output_file,

    top_n=50,

):
    """
    Generate expression heatmap using the
    most variable genes.
    """

    count_matrix = Path(count_matrix)

    output_file = Path(output_file)

    if not count_matrix.exists():

        raise FileNotFoundError(

            f"\nCount matrix not found:\n"

            f"{count_matrix}"

        )

    counts = pd.read_csv(

        count_matrix,

        index_col=0,

    )

    # ------------------------------------------
    # Select most variable genes
    # ------------------------------------------

    variance = counts.var(

        axis=1

    )

    counts = counts.loc[

        variance.nlargest(

            top_n

        ).index

    ]

    # ------------------------------------------
    # Z-score normalization
    # ------------------------------------------

    counts = counts.sub(

        counts.mean(axis=1),

        axis=0,

    )

    counts = counts.div(

        counts.std(axis=1),

        axis=0,

    )

    plt.figure(

        figsize=(10, 10)

    )

    plt.imshow(

        counts,

        aspect="auto",

        interpolation="nearest",

    )

    plt.colorbar(

        label="Z-score"

    )

    plt.xticks(

        np.arange(

            len(counts.columns)

        ),

        counts.columns,

        rotation=90,

        fontsize=8,

    )

    plt.yticks(

        np.arange(

            len(counts.index)

        ),

        counts.index,

        fontsize=5,

    )

    plt.xlabel(

        "Samples"

    )

    plt.ylabel(

        "Genes"

    )

    plt.title(

        "Top Variable Gene Expression Heatmap"

    )

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

        f"✅ Heatmap generated:\n"

        f"{output_file}"

    )

    return output_file