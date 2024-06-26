#!/usr/bin/env python

from app import createApp
from scripts.utils import get_time
from config import Config
import os
import logging

logging.basicConfig(level = logging.DEBUG)

logging.info(f"[{get_time()}]: Checking for app/instance")
if not os.path.exists(Config.INSTANCE_FOLDER_PATH):
    logging.info(f"[{get_time()}]: Creating app/instance directory")
    os.makedirs(Config.INSTANCE_FOLDER_PATH)
else:
    pass

logging.info(f"[{get_time()}]: Checking for app/instance/reports")
if not os.path.exists(Config.REPORTS_FOLDER_PATH):
    logging.info(f"[{get_time()}]: Creating app/instance/reports directory")
    os.makedirs(Config.REPORTS_FOLDER_PATH)
else:
    pass

application = createApp()

if __name__ == "__main__":
    application.run(debug = True)