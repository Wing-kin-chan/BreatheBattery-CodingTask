import logging
from scripts.utils import get_time

def parseAirData(data: dict) -> dict:
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

