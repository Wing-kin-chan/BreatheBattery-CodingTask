#!/usr/bin/env python

from flask import Flask
from config import Config
from routes import pages
from models.db import init_db
from dash import Dash, html


app = Flask(__name__)
app.config.from_object(Config)
dash_app = Dash(__name__, 
                server = app,
                url_base_pathname = '/dash/')
dash_app.layout = html.Div()
app.extensions['dash'] = dash_app

def createApp():
    app.register_blueprint(pages)

    with app.app_context():
        init_db()
        
    return app