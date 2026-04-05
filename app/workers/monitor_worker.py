from app import database
from datetime import datetime, timedelta
from sqlalchemy import select
from app.models import Monitor, MonitorRun
from app.scrapers import google_flights_page

# freq verificacao
INTERVAL_SECONDS = 60


def utcnow():
    return datetime.now()

def get_active_monitors():
    db = database.get_session()
    try:
        query = select(Monitor).where(Monitor.is_active.is_(True))
        monitors = db.execute(query).scalars().all()
    finally:
        db.close()

    return monitors


def should_run(monitor):
    if monitor.next_run_at is None:
        return True
    
    return monitor.next_run_at <= utcnow()

def finish_success(db, monitor, offers, min_price, start_time):
    now  = utcnow()
    run = MonitorRun(
        monitor_id = monitor.id,
        status='sucess',
        offers_count = offers,
        started_at = start_time,
        finished_at= now,
        min_price = min_price

    )
    monitor.last_run_at = now
    monitor.next_run_at = now + timedelta(hours=monitor.frequency_hours)
    monitor.last_status = 'success'

    
    db.add(run)
    

def finish_error(db, monitor, e):
    now  = utcnow()
    run = MonitorRun(
        monitor_id = monitor.id,
        status='failed',
        error_message = str(e)

    )

    monitor.last_run_at = now
    monitor.next_run_at = now + timedelta(hours=monitor.frequency_hours)
    monitor.last_status = 'failed'

    
    db.add(run)
    
    
def execute_monitor(monitor):
    google = google_flights_page()
    db = database.get_session()
    try:
        offers_count, min_price, start_time = google.run_scraper(monitor)
        finish_success(db, monitor, offers_count, min_price, start_time)

    except Exception as e:
        finish_error(db, monitor, e)


    db.commit()
    db.close()


def worker_run():
    print('worker funfando')
    monitors = get_active_monitors()

    for monitor in monitors:
        if should_run(monitor):
            execute_monitor(monitor)


worker_run()

   