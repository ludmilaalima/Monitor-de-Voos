from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.db import SessionLocal, engine
from app.models import Base, Monitor, MonitorRun
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date, datetime


app = FastAPI(title='Monitor de Voos')

app.mount("/static", StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates(directory='app/templates')



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/monitores', response_class=HTMLResponse)
def home_monitors(request: Request):
    return templates.TemplateResponse('list.html', {"request": request})

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('create-monitor.html', {"request": request})


@app.get('/health')
def health():
    return {'status':'ok'}

@app.post('/api/create-monitor')
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
        frequency_hours=int(payload.get('frequency_hours', 6))
        #is_active = bool(payload.get('is_active'), True),
        #adults = int(payload.get('adults'), 1))
        )

    db.add(m)
    db.commit()
    db.refresh(m)

    print('deu bom pae')
    
    return {
        'id':m.id
    }
    
"""
refatorar pra pydantic
"""
@app.get('/api/monitors')
def list_monitors(db: Session = Depends(get_db)):
    #return db.query(Monitor).all()
    print('entrou aqui')
    q = select(Monitor)
    monitors = db.execute(q).scalars().all()
    return [{'id': m.id, 'origin_iata': m.origin_iata, 'destination_iata' : m.destination_iata} for m in monitors] 

    

@app.post('/monitors/{monitor_id}/run')
def create_run_monitor(monitor_id, db: Session = Depends(get_db)):
    monitor = db.get(Monitor, monitor_id)
    if not monitor:
        raise HTTPException(status_code=404, detail='monitor not found or not exist')
    
    run = MonitorRun(monitor_id=monitor_id, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)
    

    # por enquanto....
    price_cents = [2100, 3600, 1000]
    offers_count = len(price_cents)
    min_price = min(price_cents) if price_cents else None

    #run = sucess_run(db, run, offers_count, min_price)
   
    return {"run_id": run.id, "status": run.status, "offers_count": run.offers_count, "min_price_cents": run.min_price}


#depois rodar c airflow
def sucess_run(db, run: MonitorRun, offers_count: int, min_price: int):
    run.status = 'success' if offers_count > 0 else "empty"
    run.offers_count = offers_count
    run.min_price = min_price if min_price > 0 else None
    run.finished_at = datetime.now()

    db.commit()
    db.refresh(run)
    return run

@app.get("/monitors/{monitor_id}/runs")
def list_runs(monitor_id, db: Session = Depends(get_db)):
    monitor = db.get(Monitor, monitor_id)
    if not monitor:
        raise HTTPException(status_code=404, detail='monitor not found or not exist')
    
    q = select(MonitorRun).where(MonitorRun.monitor_id == monitor_id).order_by(MonitorRun.started_at)
    runs = db.execute(q).scalars().all()

    return [{'id': run.id,
            'monitor_id': run.monitor_id,
            'status': run.status

            } 
        
            
            for run in runs]






