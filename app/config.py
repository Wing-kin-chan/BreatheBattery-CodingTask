#!/usr/bin/env python

import os

class Config:
    SECRET_KEY = "QIU39hfkiauhiOIEHRdhf38yy395jKBILFIHIq38yjHKH834SH"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "instance", "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False