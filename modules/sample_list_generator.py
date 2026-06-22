from pathlib import Path


def generate_sample_list(
    stringtie_directory,
    output_file,
):
    """
    Create sample_list.txt for prepDE.py3.

    Format

    sample_id<TAB>path_to_gtf
    """

    stringtie_directory = Path(
        stringtie_directory
    )

    output_file = Path(output_file)

    if not stringtie_directory.exists():

        raise FileNotFoundError(

            "\nStringTie directory not found:\n"

            f"{stringtie_directory}"

        )

    gtf_files = sorted(

        stringtie_directory.glob("*.gtf")

    )

    if len(gtf_files) == 0:

        raise FileNotFoundError(

            "\nNo GTF files found."

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

        for gtf in gtf_files:

            sample = gtf.stem

            f.write(

                f"{sample}\t{gtf.resolve()}\n"

            )

    print()

    print("=" * 60)

    print(

        "Sample list generated."

    )

    print(

        f"Samples : {len(gtf_files)}"

    )

    print(

        f"Output  : {output_file}"

    )

    print("=" * 60)

    return output_file