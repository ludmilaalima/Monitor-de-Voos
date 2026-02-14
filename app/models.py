from .bd import Base
from sqlalchemy.orm import Mapped, mapped_column, SessionTransactionOrigin
from sqlalchemy import String, Date, Integer, Boolean
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
    return_date: Mapped[datetime | None] = mapped_column(Date, nullable=None)
    adults: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    frequency_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=6)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    create_at: Mapped[datetime] = mapped_column(Date, nullable=False, default=utcnow())

    





      
