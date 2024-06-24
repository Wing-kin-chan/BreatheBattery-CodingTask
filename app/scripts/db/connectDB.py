#!/usr/bin/env python
"""
This script handles all database connections and transactions.

Functions:
    - checkDeviceExists:
        Checks if a device with given ID is stored in the devices table. Returns true or false.
    
    - addDevice:
        Inserts new device into the Devices table.

    - updateDeviceLastSeen:
        Updates the value of the last_updated column for a record in the Devices table.

    - storeDeviceLog:
        Stores device log data and air data measurements in the AirData table.

    - getDeviceLastSeen:
        Retrieves the last seen date of a specified device. Returns datetime or none.

    - getDeviceData:
        Retrieves the logs of a device from the past 7 days.

"""
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
            last_updated = None
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
        
def updateDeviceLastSeen(device_id: str, last_updated: str|datetime) -> None:
    """
    Function to update the last_updated value of a device.
    """
    if isinstance(last_updated, str):
        try:
            last_updated = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logging.error(f"[{get_time()}] ValueError: Date time must be in %Y-%m-%d %H:%M:%S format.")

    with createSession() as session:
        try:
            record = session.query(Devices).filter_by(device_id = device_id).one_or_none()
        except Exception as e:
            logging.error(f"[{get_time()}] - - - - Database error: {e}")

        try:
            record.last_updated = last_updated
            session.commit()
            logging.info(f"[{get_time()}] - - - - Device record {device_id} updated. Last seen: {last_updated}")
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
            date = datetime.strptime(data['date'], "%Y-%m-%d").date(),
            time = datetime.strptime(data['time'], "%H:%M:%S").time(),
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

def getDeviceLastSeen(device_id: str) -> datetime|None:
    with createSession() as session:
        try:
            result = session.query(Devices.last_updated).filter_by(device_id = device_id).one_or_none()
            if result is not None:
                return result.last_updated
            else:
                logging.info(f"[{get_time()}] - - - - Device with ID {device_id} not found.")
                return None
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