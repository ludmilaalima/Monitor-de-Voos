from app.db import engine
from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Integer, Boolean, DateTime, ForeignKey, Text
import uuid
from datetime import datetime


def utcnow():
    return datetime.now()

class Monitor(Base):
    __tablename__ = 'monitors'
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default= str(uuid.uuid4()))
    origin_iata: Mapped[str] = mapped_column(String(3), nullable=False)
    destination_iata: Mapped[str] = mapped_column(String(3), nullable=False)
    trip_type: Mapped[str] = mapped_column(String(10), nullable=False, default='round_trip') #one way or 
    departure_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    return_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    adults: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    frequency_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=6)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(Date, nullable=False, default=utcnow())
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    next_run_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    runs: Mapped[list["MonitorRun"]] = relationship(back_populates='monitor', cascade = 'all, delete-orphan')


class MonitorRun(Base):
    __tablename__ = 'monitor_runs'
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=str(uuid.uuid4()))
    monitor_id: Mapped[str] = mapped_column(ForeignKey('monitors.id'), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utcnow())
    finished_at: Mapped[datetime |  None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(15), nullable=False, default='running')
    offers_count: Mapped[int] = mapped_column(Integer, nullable=True)
    min_price: Mapped[int | None] = mapped_column(Integer, nullable=True)

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    bronze_ref: Mapped[str | None] = mapped_column(Text, nullable=True)

    monitor: Mapped['Monitor'] = relationship(back_populates='runs')




Base.metadata.create_all(bind=engine)
    
    










      
