#!/usr/bin/env python

import logging
from scripts.utils import get_time
from typing import Generator, Dict

def parseData(data: dict) -> Generator[Dict[str, dict], None, None]:
    """
    A generator function that yields device sensor data:

    - device_info:
        - device_id
        - latitude
        - longitude
        - altitude
        - area
        - sitename
        - app_version

    - log_info:
        - time
        - date
        - device_id
        - particulates
        - humidity
        - temperature

    Parameters:

    - data: dict

    Returns:

    - data: dict
    """
    try:
        device_id = data['device_id']
    except KeyError:
        logging.error(f"[{get_time()}]: Key error, no device ID!")
        return None

    try:
        project_name = list(data['feeds'][0])[0]
    except KeyError:
        logging.error(f"[{get_time()}]: Key error, no project name for device: {device_id}")

    try:
        number_of_records = data['number_of_records']
    except KeyError:
        logging.info(f"[{get_time()}]: No number of records found.")
        number_of_records = len(data['feeds'][0][project_name])

    device_record = {'device_info': {'project': project_name},
                     'log_info': {}}

    for idx in range(0, number_of_records):
        key = list(data['feeds'][0][project_name][idx].keys())[0]
        log_data = data['feeds'][0][project_name][idx][key]

        assert log_data['device_id'] == device_id, f"Device ID in record {idx} does not match"
        device_record['device_info']['device_id'] = log_data['device_id']
        device_record['log_info']['device_id'] = log_data['device_id']

        try:
            device_record['log_info']['time'] = log_data['time']
        except KeyError:
            logging.error(f"[{get_time()}] - - - - No time data in record.")
            continue

        try:
            device_record['log_info']['date'] = log_data['date']
        except KeyError:
            logging.error(f"[{get_time()}] - - - - No date information in record.")
            continue
        
        try:
            device_record['log_info']['particulate2_5'] = float(log_data['s_d0'])
        except KeyError:
            logging.error(f"[{get_time()}] - - - - No particulate data in record.")
            continue
        except ValueError:
            logging.error(f"[{get_time()}] - - - - Bad particulate data on record.")
            continue

        try:
            device_record['device_info']['sitename'] = log_data['SiteName']
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No sitename in record.")
            pass

        try:
            device_record['device_info']['area'] = log_data['area']
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No area name in record.")
            pass
        
        try:
            device_record['device_info']['altitude'] = float(log_data['gps_alt'])
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No altitude data in record.")
            pass
        except ValueError:
            logging.info(f"[{get_time()}] - - - - Bad altitude data in record.")
            pass

        try:
            device_record['device_info']['latitude'] = float(log_data['gps_lat'])
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No latitude data in record.")
            pass
        except ValueError:
            logging.info(f"[{get_time()}] - - - - Bad latitude data in record.")
            pass

        try:
            device_record['device_info']['longitutde'] = float(log_data['gps_lon'])
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No longitude data in record.")
            pass
        except ValueError:
            logging.info(f"[{get_time()}] - - - - Bad longitude data in record.")
            pass

        try:
            device_record['log_info']['temperature'] = float(log_data['s_t0'])
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No temperature data in record.")
            pass
        except ValueError:
            logging.info(f"[{get_time()}] - - - - Bad temperature data in record.")
            pass

        try:
            device_record['log_info']['humidity'] = float(log_data['s_h0'])
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No humidity data in record.")
            pass
        except ValueError:
            logging.info(f"[{get_time()}] - - - - Bad humididty dat in record.")
            pass

        yield device_record
