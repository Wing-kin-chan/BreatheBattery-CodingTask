import logging
from scripts.utils import get_time
from typing import Generator, Dict, Any

def parseAirData(data: dict) -> Generator[Dict[str, Any], None, None]:
    """
    A generator function that yields device sensor data:

    - time
    - SiteName
    - app
    - date
    - device_id
    - particulates
    - humidity
    - temperature
    - timestamp
    - app version

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

    device_record = {}

    for idx in range(0, number_of_records):
        key = list(data['feeds'][0][project_name][idx].keys())[0]
        log_data = data['feeds'][0][project_name][idx][key]

        device_record['device_id'] = log_data['device_id']
        assert device_record['device_id'] == device_id, f"Device ID in record {idx} does not match"

        try:
            device_record['time'] = log_data['time']
        except KeyError:
            logging.error(f"[{get_time()}] - - - - No time data in record.")
            continue

        try:
            device_record['date'] = log_data['date']
        except KeyError:
            logging.error(f"[{get_time()}] - - - - No date information in record.")
            continue
        
        try:
            device_record['particulates'] = float(log_data['s_d0'])
        except KeyError:
            logging.error(f"[{get_time()}] - - - - No particulate data in record.")
            continue
        except ValueError:
            logging.error(f"[{get_time()}] - - - - Bad particulate data on record.")
            continue

        try:
            device_record['sitename'] = log_data['SiteName']
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No sitename in record.")
            pass

        try:
            device_record['area'] = log_data['area']
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No area name in record.")
            pass
        
        try:
            device_record['altitude'] = float(log_data['gps_alt'])
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No altitude data in record.")
            pass
        except ValueError:
            logging.info(f"[{get_time()}] - - - - Bad altitude data in record.")
            pass

        try:
            device_record['latitude'] = float(log_data['gps_lat'])
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No latitude data in record.")
            pass
        except ValueError:
            logging.info(f"[{get_time()}] - - - - Bad latitude data in record.")
            pass

        try:
            device_record['longitutde'] = float(log_data['gps_lon'])
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No longitude data in record.")
            pass
        except ValueError:
            logging.info(f"[{get_time()}] - - - - Bad longitude data in record.")
            pass

        try:
            device_record['temperature'] = float(log_data['s_t0'])
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No temperature data in record.")
            pass
        except ValueError:
            logging.info(f"[{get_time()}] - - - - Bad temperature data in record.")

        try:
            device_record['humidity'] = float(log_data['s_h0'])
        except KeyError:
            logging.info(f"[{get_time()}] - - - - No humidity data in record.")
            pass
        except ValueError:
            logging.info(f"[{get_time()}] - - - - Bad humididty dat in record.")
            pass

        yield device_record