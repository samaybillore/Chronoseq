import importlib
import shutil
import subprocess
import sys
from pathlib import Path

import config


# ============================================================
# REQUIRED PYTHON PACKAGES
# ============================================================

PYTHON_PACKAGES = {

    "pandas": "pandas",

    "numpy": "numpy",

    "matplotlib": "matplotlib",

    "scipy": "scipy",

    "sklearn": "scikit-learn",

}


# ============================================================
# REQUIRED EXTERNAL TOOLS
# ============================================================

TOOLS = {

    "fastqc": "fastqc",

    "multiqc": "multiqc",

    "fasterq-dump": "sra-tools",

    "trimmomatic": "trimmomatic",

    "bowtie2": "bowtie2",

    "bowtie2-build": "bowtie2",

    "samtools": "samtools",

    "stringtie": "stringtie",

    "perl": "perl",

    "Rscript": "r-base",

}


# ============================================================
# REQUIRED R PACKAGES
# ============================================================

R_PACKAGES = [

    "edgeR",

    "limma",

]


# ============================================================
# HELPER
# ============================================================

def ask_user(message):

    answer = input(

        f"{message} (Y/n): "

    ).strip().lower()

    return answer in (

        "",

        "y",

        "yes",

    )


# ============================================================
# CONDA DETECTION
# ============================================================

def has_conda():

    return (

        shutil.which("mamba") is not None

        or

        shutil.which("conda") is not None

    )


def get_installer():

    if shutil.which("mamba"):

        return "mamba"

    if shutil.which("conda"):

        return "conda"

    return None

# ============================================================
# INSTALL CONDA PACKAGE
# ============================================================

def install_conda_package(package):

    installer = get_installer()

    if installer is None:

        raise RuntimeError(

            "Conda or Mamba not found."

        )

    print(

        f"\nInstalling {package} using {installer}..."

    )

    subprocess.run(

        [

            installer,

            "install",

            "-y",

            "-c",

            "conda-forge",

            "-c",

            "bioconda",

            package,

        ],

        check=True,

    )


# ============================================================
# INSTALL PYTHON PACKAGE
# ============================================================

def install_python_package(package):

    print(

        f"\nInstalling Python package: {package}"

    )

    subprocess.run(

        [

            sys.executable,

            "-m",

            "pip",

            "install",

            package,

        ],

        check=True,

    )


# ============================================================
# CHECK PYTHON
# ============================================================

def check_python():

    version = sys.version_info

    print(

        f"Python : "

        f"{version.major}."

        f"{version.minor}."

        f"{version.micro}"

    )

    if version.major != 3:

        raise RuntimeError(

            "Python 3 is required."

        )

    if version.minor < 11:

        print(

            "⚠️ Recommended Python >= 3.11"

        )

    else:

        print(

            "✅ Python OK"

        )


# ============================================================
# CHECK PYTHON PACKAGES
# ============================================================

def check_python_packages():

    installed_anything = False

    for module_name, pip_name in PYTHON_PACKAGES.items():

        try:

            importlib.import_module(module_name)

            print(f"✅ {module_name}")

        except ImportError:

            print(f"❌ {module_name}")

            if ask_user(f"Install {pip_name}?"):

                install_python_package(pip_name)

                installed_anything = True

    return installed_anything

# ============================================================
# CHECK JAVA
# ============================================================

def check_java():

    print()

    print("=" * 60)

    print("Checking Java")

    print("=" * 60)

    if shutil.which("java") is None:

        print("❌ Java not found")

        if has_conda():

            if ask_user(

                "Install OpenJDK?"

            ):

                install_conda_package(

                    "openjdk"

                )

        else:

            print(

                "⚠️ Install Java manually "

                "or install Miniconda."

            )

        return

    result = subprocess.run(

        [

            "java",

            "-version",

        ],

        stderr=subprocess.PIPE,

        stdout=subprocess.PIPE,

        text=True,

    )

    version = (

        result.stderr.splitlines()

        or

        result.stdout.splitlines()

    )

    if version:

        print(version[0])

    print("✅ Java OK")


# ============================================================
# CHECK EXTERNAL TOOLS
# ============================================================

def check_tools():

    print()

    print("=" * 60)

    print("Checking External Tools")

    print("=" * 60)

    for executable, package in TOOLS.items():

        if shutil.which(executable):

            print(

                f"✅ {executable}"

            )

            continue

        print(

            f"❌ {executable}"

        )

        if has_conda():

            if ask_user(

                f"Install {package}?"

            ):

                install_conda_package(

                    package

                )

        else:

            print(

                "⚠️ Conda/Mamba not found."

            )

            print(

                f"Please install {package} manually."

            )


# ============================================================
# VERIFY TOOL INSTALLATION
# ============================================================

def verify_tools():

    print()

    print("=" * 60)

    print("Verifying Installation")

    print("=" * 60)

    failed = []

    for executable in TOOLS:

        if shutil.which(executable):

            print(

                f"✅ {executable}"

            )

        else:

            print(

                f"❌ {executable}"

            )

            failed.append(

                executable

            )

    if failed:

        raise RuntimeError(

            "\nThe following tools are still missing:\n\n"

            + "\n".join(failed)

        )

    print()

    print(

        "All required external tools detected."

    )

# ============================================================
# CHECK R PACKAGES
# ============================================================

def check_r_packages():

    if shutil.which("Rscript") is None:

        print()

        print("⚠️ Rscript not available. Skipping R package check.")

        return

    print()

    print("=" * 60)

    print("Checking R Packages")

    print("=" * 60)

    for package in R_PACKAGES:

        command = (

            f'if (!requireNamespace("{package}", quietly=TRUE)) '

            "{ quit(status=1) }"

        )

        result = subprocess.run(

            [

                "Rscript",

                "-e",

                command,

            ]

        )

        if result.returncode == 0:

            print(

                f"✅ {package}"

            )

            continue

        print(

            f"❌ {package}"

        )

        if ask_user(

            f"Install R package '{package}'?"

        ):

            subprocess.run(

                [

                    "Rscript",

                    "-e",

                    (

                        f'install.packages('

                        f'"{package}", '

                        'repos="https://cloud.r-project.org"'

                        ")"

                    ),

                ],

                check=True,

            )


# ============================================================
# CREATE PROJECT DIRECTORIES
# ============================================================

def create_directories():

    print()

    print("=" * 60)

    print("Checking Project Directories")

    print("=" * 60)

    directories = [

        config.DATA,

        config.RAW,

        config.METADATA_DIR,

        config.FASTQ,

        config.REFERENCE,

        config.INDEX,

        config.QC_RAW,

        config.MULTIQC_RAW,

        config.QC_TRIMMED,

        config.MULTIQC_TRIMMED,

        config.TRIMMED,

        config.ALIGNMENTS,

        config.STRINGTIE,

        config.COUNTS,

        config.RESULTS,

        config.TRINITY_RESULTS,

        config.MAPPING_STATS,

        config.PLOTS,

        config.LOGS,

        config.RESOURCES,

        config.REPORT_TEMPLATE.parent,

    ]

    for directory in directories:

        directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        print(

            f"✅ {directory}"

        )


# ============================================================
# CREATE DEFAULT FILES
# ============================================================

def create_default_files():

    print()

    print("=" * 60)

    print("Checking Required Files")

    print("=" * 60)

    # --------------------------------------------------------

    # metadata.csv

    # --------------------------------------------------------

    if not config.METADATA.exists():

        config.METADATA.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        config.METADATA.write_text(

            "sample_id,condition,replicate\n"

            "SRR000001,Control,1\n"

            "SRR000002,Control,2\n"

            "SRR000003,Treated,1\n"

            "SRR000004,Treated,2\n"

        )

        print(

            "✅ Created metadata.csv"

        )

    else:

        print(

            "✅ metadata.csv exists"

        )

    # --------------------------------------------------------

    # log file

    # --------------------------------------------------------

    if not config.LOG_FILE.exists():

        config.LOG_FILE.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        config.LOG_FILE.touch()

        print(

            "✅ Created CHRONOSEQ.log"

        )

    else:

        print(

            "✅ CHRONOSEQ.log exists"

        )

    # --------------------------------------------------------

    # adapters

    # --------------------------------------------------------

    if not config.ADAPTERS.exists():

        raise FileNotFoundError(

            "\n"

            "❌ Adapter file not found.\n\n"

            f"Expected:\n"

            f"{config.ADAPTERS}\n\n"

            "Please place TruSeq3-PE.fa "

            "inside resources/adapters/"

        )

    print(

        "✅ Adapter file found"

    )

# ============================================================
# RUN COMPLETE SETUP
# ============================================================

def run_setup():

    print()

    print("=" * 60)

    print("🧬 CHRONOSEQ SETUP")

    print("=" * 60)

    # --------------------------------------------------------
    # Python
    # --------------------------------------------------------

    python_packages_installed = check_python_packages()

    check_python()

    # --------------------------------------------------------
    # Python packages
    # --------------------------------------------------------

    check_python_packages()

    # --------------------------------------------------------
    # Java
    # --------------------------------------------------------

    check_java()

    # --------------------------------------------------------
    # External tools
    # --------------------------------------------------------

    check_tools()

    # --------------------------------------------------------
    # Verify tools
    # --------------------------------------------------------

    verify_tools()

    # --------------------------------------------------------
    # R packages
    # --------------------------------------------------------

    check_r_packages()

    # --------------------------------------------------------
    # Directories
    # --------------------------------------------------------

    create_directories()

    # --------------------------------------------------------
    # Required files
    # --------------------------------------------------------

    create_default_files()

    print()

    print("=" * 60)

    print("🎉 CHRONOSEQ SETUP COMPLETED SUCCESSFULLY")

    print("=" * 60)

    print()

    print("You are ready to run the pipeline.")

    print()

    print("Project structure checked.")

    print("Dependencies checked.")

    print("Metadata template ready.")

    print("Logging initialized.")

    print()

    print("=" * 60)

    print("🧬 HAPPY ANALYZING WITH CHRONOSEQ")

    print("=" * 60)

    print()

