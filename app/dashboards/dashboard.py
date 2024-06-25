#!/usr/bin/env python

from scripts.db.connectDB import getDeviceData, getDeviceMeta
from scripts.logic import plot, processData
from scripts.utils import get_time
from dash import dcc, html
from datetime import datetime
import logging

logging.basicConfig(level = logging.DEBUG)

def layout(device_id = None):
    try:
        logging.info(f"[{get_time()}] - - - - Retrieving device data for {device_id}")
        data = getDeviceData(device_id)
        logging.info(f"[{get_time()}] - - - - Retrieving device metadata for {device_id}")
        metadata = getDeviceMeta(device_id)
    except Exception as e:
        logging.error(f"[{get_time()}] - - - - Unable to retrieve data for device: {device_id}")
        return f"Error {e}: Unable to retrieve data for device {device_id}"
    
    daily_stats = plot.dailyStatistics(data)
    line_graph = plot.lineChart(data)

    dash_layout = html.Div([
        html.H1(f"{device_id} Historical Data"),
        html.H3("Particulate 2.5 data from today and the previous 7 days"),
        html.Div([
            html.H4("Device Information:"),
            html.P(f"Device ID: {device_id}"),
            html.P(f"Project: {metadata.project}"),
            html.P(f"GPS Latitude: {metadata.latitude}"),
            html.P(f"GPS Longitude: {metadata.longitude}"),
            html.P(f"GPS Altitude: {metadata.altitude}"),
            html.P(f"Device Areaname: {metadata.area}"),
            html.P(f"Device Sitename: {metadata.sitename}"),
            html.P(f"Time of latest record: {datetime.strftime(metadata.last_updated, '%H:%M:%S %d-%m-%Y')}")
        ]),
        dcc.Graph(figure = daily_stats),
        dcc.Graph(figure = line_graph)
    ])

    return dash_layout