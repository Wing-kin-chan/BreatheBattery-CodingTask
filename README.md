# Breathe Battery Technical Coding Task

## Summary

This project was provided as a technical assessment during the application for the role of 
Data Engineer. The goal of this project was to create a simple program which interfaces with the 
[LASS PM2.5 Open Data Portal](https://pm25.lass-net.org/), fetches and stores data, and generates
reports.

## Project Goals

- Read data from the `/device/<device_id>/history` endpoint
- Save data into local persistant storage
- Detect periods where PM2.5 levels go above the threshold of 30
- Output a report containing:
    - A list of times when the level of PM2.5 exceeded the threshold of 30
    - The daily maximum, minimum, and average PM2.5 levels
- If new data becomes available, the program should insert it into storage while maintaining pre-existing data

## Implimentation

I create a simple Flask application with a data pipeline that searches for a queried device and stores to a SQL database. Data from the last seven days is then displayed to the user through a Plotly Dash frontend. The program also generates reports as `.csv` files which the user can download.

## How to run

Clone the git repository, and create a environment and install dependencies in `requirements.txt` then run the `run.py` file:

1. `cd 'directory'`
2. `git clone git@github.com:Wing-kin-chan/BreatheBattery-CodingTask.git`
3. `pip install virtualenv`
4. `virtualenv LASS-Viewer`
5. `source LASS-Viewer/bin/activate`
6. `pip install -r requirements.txt`
7. Open browser and navigate to `http://127.0.0.1:5000`
