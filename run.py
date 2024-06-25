#!/usr/bin/env python

from app import createApp
from scripts.utils import get_time
import os
import logging

logging.basicConfig(level = logging.DEBUG)

logging.info(f"[{get_time()}]: Checking for app/instance")
if not os.path.exists(os.path.join('app', 'instance')):
    logging.info(f"[{get_time()}]: Creating app/instance folder")
    os.makedirs(os.path.join('app', 'instance'))
else:
    pass

application = createApp()

if __name__ == "__main__":
    application.run(debug = True)