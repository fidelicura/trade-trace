from datetime import datetime, timedelta
from logging import logging, INFO
from os import getenv



configure_logging(logging, INFO)

def read_keys() -> (str, str):
    try:
        API_KEY = getenv("API_KEY")
        SECRET_KEY = getenv("SECRET_KEY")

        return (API_KEY, SECRET_KEY)
    except Exception as err:
        logging.info("unable to read `API_KEY` and/or `SECRET_KEY` variables")
        raise err

def calculate_time_delta() -> (str, str):
    time_format = "%Y.%m.%d"
    now = datetime.now()

    start = now.strftime(time_format)
    end = (now - timedelta(weeks=4)).strftime(time_format)

    return (start, end)
