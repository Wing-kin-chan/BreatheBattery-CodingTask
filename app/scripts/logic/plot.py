#!/usr/bin/env python

from datetime import datetime
from models.db import AirData
from plotly.graph_objects import Figure
import pandas as pd
import plotly.express as px

def dailyStatistics(data: list[AirData]) -> Figure:
    processed_data = [(record.date, record.time, record.particulate2_5) for record in data]
    df = pd.DataFrame(processed_data, columns = ['Date', 'Time', 'PM2.5'])

    fig = px.box(df,
                 x = 'Date',
                 y = 'PM2.5',
                 title = 'Daily PM2.5 Levels',
                 hover_data = 'Time')
    
    return fig

def lineChart(data: list[AirData]) -> Figure:
    processed_data = [(record.date, record.time, record.particulate2_5) for record in data]
    df = pd.DataFrame(processed_data, columns = ['Date', 'Time', 'PM2.5'])
    df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))

    fig = px.line(df,
                  x = 'Datetime',
                  y = 'PM2.5',
                  title = 'Continuous PM2.5 Levels')
    
    return fig