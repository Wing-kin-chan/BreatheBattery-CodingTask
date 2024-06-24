#!/usr/bin/env python

from scripts.utils import get_time
from scripts.db.fetchData import getDeviceHistory
from scripts.db.parseData import parseData
from scripts.db.connectDB import *
from datetime import datetime
import logging

logging.basicConfig(level = logging.DEBUG)

def getNewData(device_id: str) -> None:
    """
    Function to get new data for a device and store in database.
    """

    try:
        data = getDeviceHistory(device_id)
    except Exception:
        return None

    if not checkDeviceExists(device_id):
        for record in parseData(data):
            if record['device_info']:
                try:
                    addDevice(record['device_info'])
                    break
                except Exception:
                    continue
    
    try:
        last_updated = getDeviceLastSeen(device_id)
    except Exception:
        return None
    
    latest_record_time = None
    for record in parseData(data):
        date = datetime.strptime(record['log_info']['date'], "%Y-%m-%d").date()
        time = datetime.strptime(record['log_info']['time'], "%H:%M:%S").time()
        record_datetime = datetime.combine(date, time)
        
        if last_updated is None or record_datetime > last_updated:
            if latest_record_time is None or record_datetime > latest_record_time:
                latest_record_time = record_datetime

            try:
                storeDeviceLog(record['log_info'])
            except Exception as e:
                logging.error(f"[{get_time()}] - - - - {device_id}: Unable to store record {date}, {time}.")
                continue
        else:
            logging.info(f"[{get_time()}] - - - - Log out of date.")
            continue
        
    if latest_record_time:
        updateDeviceLastSeen(device_id, latest_record_time)
