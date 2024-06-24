#!/usr/bin/env python

import logging, requests
from scripts.utils import get_time

logging.basicConfig(level = logging.INFO)

def getDeviceHistory(device_id: str) -> dict:
    """
    Function to get 7 day device history from HTTP endpoint.

    Parameters:
        - device_id: str

        Device ID (usually MAC Address)

    Returns:
        - data: dict

        Device data with schema:

            - device_id

            - source

            - num_of_records

            - feeds:

                - [0]:

                    - project:

                        - [Record Number]:

                            - timestamp:

                                - time
                                - SiteName
                                - app
                                - date
                                - device_id
                                - s_d0 (PM2.5 concentration)
                                - s_h0 (Humidity %)
                                - s_t0 (Temperature degrees C)
                                - timestamp
                                - app version

            - version
    """

    logging.info(f"[{get_time()}]: Getting data for device: {device_id}")
    url = f"https://pm25.lass-net.org/API-1.0.0/device/{device_id}/history/?format=JSON"

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        logging.error(f"[{get_time()}] - - - - Connection error: {e}")
    except requests.exceptions.TooManyRedirects as e:
        logging.error(f"[{get_time()}] - - - - Too many redirects: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"[{get_time()}] - - - - Request exception: {e}")

    if response.status_code == 200:
        logging.info(f"[{get_time()}] - - - - Request status: 200")
        try:
            data = response.json()
            return data
        except requests.exceptions.JSONDecodeError as e:
            logging.error(f"[{get_time()}] - - - - JSON Decode error: {e}")
            return None
    else:
        status = response.status_code
        logging.error(f"[{get_time()}] - - - - Request status: {status}")