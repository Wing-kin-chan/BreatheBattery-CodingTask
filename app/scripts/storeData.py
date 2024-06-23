#!/usr/bin/env python

from sqlalchemy import create_engine
from models.db import createSession, Devices, AirData
from scripts.utils import get_time
from datetime import datetime
import logging

import sys
sys.path.insert(1, './')
from config import Config

DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URI, echo = True)


def addDevice(data: dict) -> None:
    """
    Function to store device metadata in local database.
    """
    with createSession() as session:
        new_device = Devices(
            device_id = data['device_id'],
            project = data['project'],
            latitude = data.get('latitude'),
            longitude = data.get('longitude'),
            altitude = data.get('altitude'),
            area = data.get('area'),
            sitename = data.get('sitename'),
            app_version = data.get('app_version'),
            last_updated = datetime
        )

        try:
            session.add(new_device)
            logging.info(f"[{get_time()}] - - - - Added new device: {data['device_id']}")
        except Exception as e:
            logging.error(f"[{get_time()}] - - - - Database error: {e}")
            session.rollback()
        try:
            session.commit()
            logging.info(f"[{get_time()}] - - - - Committing changes.")
        except Exception as e:
            logging.error(f"[{get_time()}] - - - - Database error: {e}")
            session.rollback()     
        finally:
            session.close()
            return None

def storeDeviceLog(data: dict) -> None:
    """
    Function to store device log data in local database.
    """
    with createSession() as session:
        new_log = AirData(
            device_id =  data['device_id'],
            date = data['date'],
            time = data['time'],
            temperature = data.get('temperature'),
            humidity = data.get('humidity'),
            particulate2_5 = data['particulate2_5']
        )

        try:
            session.add(new_log)
            logging.info(f"[{get_time()}] - - - - Saving log: {data['time'], data['date']}")
        except Exception as e:
            logging.error(f"[{get_time()}] - - - - Database error: {e}")
            session.rollback()
        try:
            session.commit()
            logging.info(f"[{get_time()}] - - - - Committing changes.")
        except Exception as e:
            logging.error(f"[{get_time()}] - - - - Database error: {e}")
            session.rollback()
        finally:
            session.close()
            return None
        