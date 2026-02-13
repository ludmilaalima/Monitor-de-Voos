from .bd import Base
from sqlalchemy.orm import Mapped, mapped_column, SessionTransactionOrigin
from sqlalchemy import String
import uuid

class Monitor(Base):
    __tablename__ = 'monitors'
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default= str(uuid.uuid4()))
    origin_iata: Mapped[str] = mapped_column(String(3), nullable=False)
    destination_iata: Mapped[str] = mapped_column(String(3), nullable=False)
      
