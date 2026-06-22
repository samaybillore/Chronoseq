from pathlib import Path


def create_processing_plan(metadata, files):
    """
    Create processing plan by matching metadata
    sample IDs to raw sequencing files.

    Parameters
    ----------
    metadata : pandas.DataFrame

    files : list[Path]

    Returns
    -------
    list[dict]
    """

    plan = []

    file_lookup = {}

    # ------------------------------------------
    # Index files by stem
    # ------------------------------------------

    for file in files:

        file_lookup[file.stem] = file

    # ------------------------------------------
    # Match metadata
    # ------------------------------------------

    for _, row in metadata.iterrows():

        sample_id = str(row["sample_id"])

        if sample_id not in file_lookup:

            raise FileNotFoundError(

                "\n"

                f"Raw sequencing file for "

                f"'{sample_id}' not found."

            )

        plan.append(

            {

                "sample_id": sample_id,

                "condition": str(

                    row["condition"]

                ),

                "replicate": int(

                    row["replicate"]

                ),

                "file": str(

                    file_lookup[sample_id]

                ),

            }

        )

    # ------------------------------------------
    # Display plan
    # ------------------------------------------

    print()

    print("=" * 60)

    print("PROCESSING PLAN")

    print("=" * 60)

    for sample in plan:

        print(

            f"{sample['sample_id']}"

            f" | "

            f"{sample['condition']}"

            f" | Rep "

            f"{sample['replicate']}"

        )

    print("=" * 60)

    print()

    return plan