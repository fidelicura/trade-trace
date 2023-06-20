from datetime import datetime, timedelta
from binance.spot import Spot as Client
from logging import getLogger, INFO
from typing import Tuple
from os import getenv



logger = getLogger("binance_app")
logger.setLevel(INFO)


def read_keys() -> Tuple[str, str]:
    try:
        API_KEY = getenv("API_KEY")
        SECRET_KEY = getenv("SECRET_KEY")

        if API_KEY == None or SECRET_KEY == None:
            raise ValueError("`API_KEY` and/or `SECRET_KEY` environment variables are not set")
        else:
            return (API_KEY, SECRET_KEY)
    except Exception as err:
        logger.info("unable to read `API_KEY` and/or `SECRET_KEY` variables")
        raise err

def create_client() -> Client:
    API_KEY, SECRET_KEY = read_keys()
    return Client(API_KEY, SECRET_KEY)

def calculate_time_delta() -> Tuple[str, str]:
    time_format = "%Y.%m.%d"
    now = datetime.now()

    start = now.strftime(time_format)
    end = (now - timedelta(weeks=4)).strftime(time_format)

    return (start, end)
