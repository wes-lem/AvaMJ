"""
Cron Job: puxa notas do Moodle em intervalo definido (APScheduler).
"""
from apscheduler.schedulers.background import BackgroundScheduler

from backend.services.moodle_client import sync_grades_from_moodle


def sync_grades_job():
    """Tarefa agendada: sincronizar notas do Moodle."""
    sync_grades_from_moodle()


def start_scheduler():
    """Inicia o agendador em background."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_grades_job, "interval", hours=1)
    scheduler.start()
