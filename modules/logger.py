from datetime import datetime
from pathlib import Path
import time


class CHRONOSEQLogger:
    """
    CHRONOSEQ Pipeline Logger
    ----------------------
    Handles:

    • General logging
    • Stage timing
    • Runtime summary
    """

    def __init__(self, log_file):

        self.log_file = Path(log_file)

        self.log_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.pipeline_start = time.perf_counter()

        self.stage_start_times = {}

        self.stage_durations = {}

    # --------------------------------------------------
    # Generic logging
    # --------------------------------------------------

    def info(self, message):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as log:

            log.write(
                f"[{timestamp}] {message}\n"
            )

    # --------------------------------------------------
    # Stage start
    # --------------------------------------------------

    def stage_start(self, stage):

        self.stage_start_times[stage] = time.perf_counter()

        self.info(
            f"▶ STARTED : {stage}"
        )

    # --------------------------------------------------
    # Stage end
    # --------------------------------------------------

    def stage_end(self, stage):

        if stage not in self.stage_start_times:

            raise KeyError(
                f"{stage} was never started."
            )

        elapsed = (

            time.perf_counter()

            - self.stage_start_times[stage]

        )

        self.stage_durations[stage] = elapsed

        self.info(

            f"✔ COMPLETED : "

            f"{stage} "

            f"({elapsed:.2f} sec)"

        )

    # --------------------------------------------------
    # Runtime summary
    # --------------------------------------------------

    def runtime_summary(self):

        total_runtime = (

            time.perf_counter()

            - self.pipeline_start

        )

        self.info("")

        self.info("=" * 60)

        self.info("CHRONOSEQ RUNTIME SUMMARY")

        self.info("=" * 60)

        for stage, runtime in self.stage_durations.items():

            self.info(

                f"{stage:<40}"

                f"{runtime:>10.2f} sec"

            )

        self.info("-" * 60)

        self.info(

            f"{'TOTAL PIPELINE TIME':<40}"

            f"{total_runtime:>10.2f} sec"

        )

        self.info("=" * 60)