from time import sleep
from datetime import datetime
from src.general import read_keys
from binance.error import ClientError
from binance.spot import Spot as Client
from typing import Tuple, Union, Dict, NoReturn

REQ_URL = "https://api.binance.com/api/v3/exchangeInfo?symbol="



def pair_info(text: str) -> Tuple[str, str, str]:
    try:
        curr_left, curr_right = text.split("/")
    except ValueError as err:
        print("Invalid input. Provide right pair, e.g. USDT/BTC")
        process_arbitrage()

    return (curr_left, curr_right, f"{curr_left}{curr_right}")

def make_request(client: Client, symbol: str) -> Tuple[Dict[str, Union[str, int]], Client]:
    response = client.avg_price(symbol)

    return (response, client)

def handle_info(text: str, pair: Tuple[str, str], info: Tuple[Dict[str, Union[str, int]], Client]) -> NoReturn:
    try:
        info, client = info[0], info[1]
        price = info["price"]
        now = datetime.now().strftime("%H:%M:%S")

        print(f"\n[{now}] Price of {pair[0]} by {pair[1]} is {price}")
        sleep(2) # not to kill API limits
        process_arbitrage(client, text)
    except KeyboardInterrupt as user_interrupt:
        print("Closing program. Thanks for your usage!")
        exit()



def process_arbitrage(client: Client, user_text: str):
    try:
        curr_pair = pair_info(user_text)
    except ValueError as err:
        print("Invalid input, please enter a currency with with a \"/\" separator, e.g. USDT/BTC")
        return process_arbitrage()

    response = make_request(client, curr_pair[2])
    handle_info(user_text, (curr_pair[0], curr_pair[1]), response)
