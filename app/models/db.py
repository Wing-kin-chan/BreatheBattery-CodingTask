#!/usr/bin/env python

from sqlalchemy import PrimaryKeyConstraint, ForeignKey
from sqlalchemy import String, Date, Time, Float, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session, scoped_session
from sqlalchemy.orm import Mapped, registry
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from scripts.utils import get_time
import logging

import sys
sys.path.insert(1, './')
from config import Config

logging.basicConfig(level = logging.INFO)

mapper_registry = registry()
DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URI, echo = True)

class Base(DeclarativeBase):
    pass

class Devices(Base):
    __tablename__ = "Devices"

    device_id: Mapped[str] = mapped_column(String(64), primary_key = True)
    project: Mapped[str] = mapped_column(String(32), nullable = False)
    latitude: Mapped[float] = mapped_column(Float(32), nullable = True)
    longitude: Mapped[float] = mapped_column(Float(32), nullable = True)
    altitude: Mapped[float] = mapped_column(Float(16), nullable = True)
    area: Mapped[str] = mapped_column(String(32), nullable = True)
    sitename: Mapped[str] = mapped_column(String(64), nullable = True)
    app_version: Mapped[str] = mapped_column(String(12), nullable = True)
    last_updated: Mapped[DateTime] = mapped_column(DateTime, nullable = True)

    air_data: Mapped[list["AirData"]] = relationship("AirData", 
                                                     back_populates = "device",
                                                     cascade = "all, delete-orphan")

class AirData(Base):
    __tablename__ = "AirData"

    device_id: Mapped[str] = mapped_column(String(64), ForeignKey('Devices.device_id'), nullable = False)
    date: Mapped[Date] = mapped_column(Date, nullable = False)
    time: Mapped[Time] = mapped_column(Time, nullable = False)
    temperature: Mapped[float] = mapped_column(Float(16), nullable = True)
    humidity: Mapped[float] = mapped_column(Float(16), nullable = True)
    particulate2_5: Mapped[float] = mapped_column(Float(16), nullable = False)

    device: Mapped['Devices'] = relationship('Devices', back_populates = 'air_data')

    __table_args__ = (
        PrimaryKeyConstraint('device_id', 'date', 'time', name = 'device_log_PK'),
    )

def init_db() -> None:
    Base.metadata.create_all(bind = engine)
    return None

def createSession() -> Session:
    try:
        Session = scoped_session(sessionmaker(bind = engine))
        session = Session()
        logging.info(f"[{get_time()}] - - - - Connected to database!")
        return session
    except Exception as e:
        logging.error(f"[{get_time()}] - - - - Unable to connect to database: {e}")