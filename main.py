from fastapi import FastAPI, HTTPException, Depends
from app.db import SessionLocal, engine
from app.models import Base, Monitor
from sqlalchemy.orm import Session
from sqlalchemy import select


app = FastAPI(title='Monitor de Voos')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def health():
    return {'status':'ok'}

def create_monitor(payload, db: Session = Depends(get_db)):
    required = ['origin_iata', 'destination_iata', 'departure_date', 'trip_type']
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
        departure_date = payload['departure_iata'],
        return_date = payload.get('return_date') ,
        frequency_hours=int(payload.get('frequency_hours', 6)),
        is_active = bool(payload.get('is_active'), True),
        adults = int(payload.get('adults'), 1))

    db.add(m)
    db.commit()
    db.refresh(m)
    return {
        'id':m.id
    }
    

def list_monitors(db: Session = Depends(get_db)):
    return db.query(Monitor).all()


    


    