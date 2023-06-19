from requests import request
from src.general import logger

REQ_URL = "https://api.binance.com/api/v3/exchangeInfo?symbol="



def pair_info() -> (str, str):
    user_text = "Enter your currency pair (from Spot trading, e.g. USDT/RUB): "
    (curr_left, curr_right) = input(user_text).split()

    return (curr_left, curr_right)

def make_request(curr_left, curr_right):
    symbol = curr_left + curr_right
    req = request("GET", REQ_URL + symbol)
    print(req)



def process_arbitrage():
    (curr_left, curr_right) = pair_info()
    make_request(curr_left, curr_right)
