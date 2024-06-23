#!/usr/bin/env python

from sqlalchemy import create_engine, and_
from models.db import createSession, Devices, AirData
from scripts.utils import get_time
from datetime import datetime, timedelta
import logging

import sys
sys.path.insert(1, './')
from config import Config

DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URI, echo = True)

def checkDeviceExists(device_id: str) -> bool:
    """
    Function that checks whether a device with certain ID exists.

    Parameters:
        - device_id: str

    Returns:
        - exists: bool
    """
    with createSession() as session:
        try:
            exists = session.query(Devices).filter_by(device_id = device_id).first() is not None
            return exists
        except Exception as e:
            logging.error(f"[{get_time()}] - - - - Database error: {e}")
        finally:
            session.close()


def getDeviceData(device_id: str):
    """
    Function to retrieve the last 7 days of device data from the database.
    """
    time = datetime.now() - timedelta(days = 7)
    with createSession() as session:
        try:
            data_objects = session.query(AirData).filter(
                and_(
                    AirData.device_id == device_id,
                    AirData.date >= time.date()
                )
            ).all()
            return data_objects
        except Exception as e:
            logging.error(f"[{get_time()}] - - - - Database error: {e}")
            session.rollback()
        finally:
            session.close()