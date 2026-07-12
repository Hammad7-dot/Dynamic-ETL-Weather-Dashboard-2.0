from apscheduler.schedulers.background import BackgroundScheduler

from config.settings import DEFAULT_CITIES
from etl.pipeline import run_pipeline_multi
from utils.logger import logger

scheduler = BackgroundScheduler()

# Module-level flag (not st.session_state!) - Streamlit re-runs the whole
# script on every interaction, and session_state is per-browser-tab, so the
# old "if not in session_state" check let every new tab/session spin up
# another BackgroundScheduler in the same process. This guard is shared by
# the whole process, so the job is only ever registered once.
_scheduler_started = False


def scheduled_job(cities=None):
    cities = cities or DEFAULT_CITIES
    logger.info(f"Running scheduled ETL for {cities}...")
    results = run_pipeline_multi(cities)
    failed = [c for c, r in results.items() if not r["ok"]]
    if failed:
        logger.error(f"Scheduled ETL failed for: {failed}")


def start_scheduler(cities=None, hours: int = 1):
    global _scheduler_started

    if _scheduler_started:
        return

    scheduler.add_job(
        scheduled_job,
        trigger="interval",
        hours=hours,
        args=[cities or DEFAULT_CITIES],
        id="weather_job",
        replace_existing=True,
    )

    if not scheduler.running:
        scheduler.start()

    _scheduler_started = True
