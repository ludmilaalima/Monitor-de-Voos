from fastapi import FastAPI, HTTPException, Depends, Body
from app.db import SessionLocal, engine
from app.models import Base, Monitor, MonitorRun
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date, datetime


app = FastAPI(title='Monitor de Voos')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/health')
def health():
    return {'status':'ok'}

@app.post('/monitors')
def create_monitor(payload: dict = Body(...), db: Session = Depends(get_db)):
    required = ['origin_iata', 'destination_iata', 'departure_date', 'trip_type']
    print(type(payload))
    for r in required:
        if r not in payload:
            raise HTTPException(status_code=400, detail=f'missing field: {r}')
        
    origin = str(payload['origin_iata'])
    destination = str(payload["destination_iata"])
    trip_type = str(payload['trip_type'])
    
    m = Monitor(
        origin_iata = origin,
        destination_iata = destination,
        trip_type = trip_type,
        departure_date = date.fromisoformat(payload['departure_date']),
        #return_date = date.fromisoformat(payload['return_date']),
        frequency_hours=int(payload.get('frequency_hours', 6)
        #is_active = bool(payload.get('is_active'), True),
        #adults = int(payload.get('adults'), 1))
        ))

    db.add(m)
    db.commit()
    db.refresh(m)
    return {
        'id':m.id
    }
    
"""
refatorar pra pydantic
"""
@app.get('/monitors')
def list_monitors(db: Session = Depends(get_db)):
    #return db.query(Monitor).all()
    q = select(Monitor)
    monitors = db.execute(q).scalars().all()
    return [{'id': m.id, 'origin_iata': m.origin_iata, 'destination_iata' : m.destination_iata} for m in monitors] 

    


def create_run(db, monitor_id):
    run = MonitorRun(monitor_id=monitor_id, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)
    return run

def finished_run(db, monitor_id):
    ...

def sucess_run(db, run: MonitorRun, offers_count: int, min_price_cents: int):
    run.status = 'success' if offers_count > 0 else "empty"
    run.offers_count = offers_count
    run.min_price = min_price_cents if min_price_cents > 0 else None
    run.finished_at = datetime.now()






