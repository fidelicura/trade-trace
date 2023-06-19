from datetime import datetime, timedelta
from logging import logging, INFO



configure_logging(logging, INFO)

def calculate_time_delta():
    time_format = "%Y.%m.%d"
    now = datetime.now()

    start = now.strftime(time_format)
    end = (now - timedelta(weeks=4)).strftime(time_format)
