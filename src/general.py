from datetime import datetime, timedelta
from logging import logging, INFO
from os import getenv



configure_logging(logging, INFO)

def read_keys():
    API_KEY = getenv("API_KEY")
    ADD_KEY = getenv("")

def calculate_time_delta():
    time_format = "%Y.%m.%d"
    now = datetime.now()

    start = now.strftime(time_format)
    end = (now - timedelta(weeks=4)).strftime(time_format)
