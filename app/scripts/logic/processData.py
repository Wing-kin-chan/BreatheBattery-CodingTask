#!/usr/bin/env python

import pandas as pd
from models.db import AirData
from datetime import datetime

THRESHOLD = 30

def getTimesAboveThreshold(data: list[AirData]) -> pd.DataFrame:
    danger_periods = []
    for record in data:
        if record.particulate2_5 > THRESHOLD:
            date = datetime.strftime(record.date, "%Y-%m-%d")
            time = datetime.strftime(record.time, "%H:%M:%S")
            danger_periods.append((date, time, record.particulate2_5))
        else:
            continue

    return pd.DataFrame(danger_periods, columns = ['Date', 'Time', 'PM2.5'])

def getDailyStatistics(data: list[AirData]) -> pd.DataFrame:
    processed_data = []
    for record in data:
        date = datetime.strftime(record.date, "%Y-%m-%d")
        processed_data.append((date, record.particulate2_5))
    
    df = pd.DataFrame(processed_data, columns = ['Date', 'PM2.5'])
    daily_statistics = df.groupby('Date')['PM2.5'].agg(['min', 'max', 'mean']).reset_index()
    daily_statistics.columns = ['Date', 'Minimum PM2.5', 'Average PM2.5', 'Maximum PM2.5']

    return daily_statistics