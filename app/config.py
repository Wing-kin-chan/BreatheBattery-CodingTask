#!/usr/bin/env python

import os
from scripts.utils import generate_key

class Config:
    SECRET_KEY = generate_key()
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    INSTANCE_FOLDER_PATH = os.path.join(BASE_DIR, "instance")
    REPORTS_FOLDER_PATH = os.path.join(BASE_DIR, INSTANCE_FOLDER_PATH, "reports")