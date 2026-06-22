from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def generate_pca_plot(

    count_matrix,

    metadata,

    output_file,

):
    """
    Generate PCA plot from
    gene count matrix.
    """

    count_matrix = Path(count_matrix)

    metadata = Path(metadata)

    output_file = Path(output_file)

    if not count_matrix.exists():

        raise FileNotFoundError(

            f"\nCount matrix not found:\n"

            f"{count_matrix}"

        )

    if not metadata.exists():

        raise FileNotFoundError(

            f"\nMetadata not found:\n"

            f"{metadata}"

        )

    counts = pd.read_csv(

        count_matrix,

        index_col=0,

    )

    meta = pd.read_csv(

        metadata

    )

    samples = meta["sample_id"].tolist()

    conditions = meta["condition"].tolist()

    counts = counts[samples]

    scaler = StandardScaler()

    scaled = scaler.fit_transform(

        counts.T

    )

    pca = PCA(

        n_components=2

    )

    coords = pca.fit_transform(

        scaled

    )

    plt.figure(

        figsize=(8, 6)

    )

    unique_conditions = sorted(

        set(conditions)

    )

    for condition in unique_conditions:

        idx = [

            i

            for i, x

            in enumerate(

                conditions

            )

            if x == condition

        ]

        plt.scatter(

            coords[idx, 0],

            coords[idx, 1],

            label=condition,

            s=80,

        )

    for i, sample in enumerate(samples):

        plt.text(

            coords[i, 0],

            coords[i, 1],

            sample,

            fontsize=8,

        )

    plt.xlabel(

        f"PC1 "

        f"({pca.explained_variance_ratio_[0]*100:.2f}%)"

    )

    plt.ylabel(

        f"PC2 "

        f"({pca.explained_variance_ratio_[1]*100:.2f}%)"

    )

    plt.title(

        "Principal Component Analysis"

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

        f"✅ PCA plot generated:\n"

        f"{output_file}"

    )

    return output_file