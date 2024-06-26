#!/usr/bin/env python

from flask import render_template, Blueprint, request, redirect, url_for, current_app, send_from_directory
from dashboards.dashboard import layout
from scripts.logic.pipeline import getNewData, checkDeviceExists
from scripts.utils import get_time
from config import Config
import logging
import os

logging.basicConfig(level = logging.DEBUG)
DOWNLOAD_FILE_PATH = Config.REPORTS_FOLDER_PATH

pages = Blueprint(name = "pages",
                import_name = __name__,
                static_folder = "static",
                template_folder = "templates")

@pages.route('/')
def index():
    return render_template("index.html")

@pages.route('/search', methods = ['POST'])
def search():
    device_id = request.form.get('device_id')
    
    #Fetch latest updated data.
    try:
        getNewData(device_id)
    except Exception:
        logging.error(f"[{get_time()}] - - - - Unable to get new data for {device_id}")
        pass
    
    #Make sure there are device records in database
    try:
        device_exists = checkDeviceExists(device_id)
        if device_exists:
            logging.info(f"[{get_time()}] - - - - {device_id} records found. Redirecting")
            return redirect(url_for('pages.dashboard', device_id = device_id))
    except Exception as e:
        logging.error(f"[{get_time()}] - - - - Error: {e}")
        return f"Error fetching data for device: {device_id}. Error message: {e}"

@pages.route('/dash/<device_id>')
def dashboard(device_id):
    dash_app = current_app.extensions['dash']
    dash_app.layout = layout(device_id)
    return redirect(f"/dash/{device_id}/")

@pages.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(directory = DOWNLOAD_FILE_PATH, path = filename)