from pathlib import Path

from datetime import datetime

import pandas as pd


def generate_html_report(

    template_file,

    output_file,

    mapping_summary,

    pca_plot,

    volcano_plot,

    heatmap_plot,

    ma_plot,

):
    """
    Generate CHRONOSEQ HTML report.
    """

    template_file = Path(template_file)

    output_file = Path(output_file)

    mapping_summary = Path(mapping_summary)

    if not template_file.exists():

        raise FileNotFoundError(

            f"\nTemplate not found:\n"

            f"{template_file}"

        )

    if not mapping_summary.exists():

        raise FileNotFoundError(

            f"\nMapping summary not found:\n"

            f"{mapping_summary}"

        )

    html = template_file.read_text(

        encoding="utf-8"

    )

    # ------------------------------------------
    # Mapping table
    # ------------------------------------------

    table = pd.read_csv(

        mapping_summary

    ).to_html(

        index=False,

        classes="table",

        border=0,

    )

    html = html.replace(

        "{{DATE}}",

        datetime.now().strftime(

            "%d %B %Y"

        ),

    )

    html = html.replace(

        "{{MAPPING_TABLE}}",

        table,

    )

    html = html.replace(

        "plots/PCA.png",

        str(Path(pca_plot).name),

    )

    html = html.replace(

        "plots/Volcano.png",

        str(Path(volcano_plot).name),

    )

    html = html.replace(

        "plots/Heatmap.png",

        str(Path(heatmap_plot).name),

    )

    html = html.replace(

        "plots/MA_Plot.png",

        str(Path(ma_plot).name),

    )

    output_file.parent.mkdir(

        parents=True,

        exist_ok=True,

    )

    output_file.write_text(

        html,

        encoding="utf-8",

    )

    print()

    print("=" * 60)

    print("HTML report generated.")

    print(f"Output : {output_file}")

    print("=" * 60)

    print()

    return output_file