from sqlalchemy import PrimaryKeyConstraint, ForeignKey
from sqlalchemy import String, Date, Time, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Mapped, registry
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from config import Config

mapper_registry = registry()
DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI

class Base(DeclarativeBase):
    pass

@Mapped
class Devices(Base):
    __tablename__ = "Devices"

    device_id: Mapped[str] = mapped_column(String(64), primary_key = True)
    project: Mapped[str] = mapped_column(String(32), nullable = False)
    latitude: Mapped[float] = mapped_column(Float(32), nullable = True)
    longitude: Mapped[float] = mapped_column(Float(32), nullable = True)

    air_data: Mapped[list["AirData"]] = relationship("AirData", 
                                                     back_populates = "Device",
                                                     cascade = "all, delete-orphan")

@Mapped 
class AirData(Base):
    __tablename__ = "AirData"

    device_id: Mapped[str] = mapped_column(String(64), ForeignKey('Devices.device_id'), nullable = False)
    date: Mapped[Date] = mapped_column(Date, nullable = False)
    time: Mapped[Time] = mapped_column(Time, nullable = False)
    temperature: Mapped[float] = mapped_column(Float(16), nullable = True)
    humidity: Mapped[float] = mapped_column(Float(16), nullable = True)
    particulate2_5: Mapped[float] = mapped_column(Float(16), nullable = True)

    device: Mapped['Devices'] = relationship('Devices', back_populates = 'air_data')

    __table_args__ = (
        PrimaryKeyConstraint('device_id', 'date', 'time', name = 'device_log_PK'),
    )

engine = create_engine(DATABASE_URI, echo = True)
Base.metadata.create_all(engine)