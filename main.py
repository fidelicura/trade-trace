from src.orders import process_orders
from src.arbitrage import process_arbitrage
from src.general import create_client



class InvalidInput(ValueError):
    pass

class WrongVariant(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def main():
    print("If you want to stop program, press CTRL+C")

    print("It's time to choose!\n1 - orders only;\n2 - arbitrage only;\n3 - both;\n")
    client = create_client()

    try:
        user_req = int(input("Your variant: "))
        print("Yes, Boss! Processing...\n")
    except ValueError:
        raise InvalidInput("Not a number. Input number from 1 to 3.")

    if user_req == 1:
        process_orders(client)
    elif user_req == 2:
        user_text = "Enter your currency pair (from Spot trading, e.g. USDT/BTC): "
        print()
        user_input = input(user_text)
        process_arbitrage(client, user_input)
    elif user_req == 3:
        user_text = "Enter your currency pair (from Spot trading, e.g. USDT/BTC): "
        print()
        user_input = input(user_text)
        process_orders(client)
        process_arbitrage(client, user_input)
    else:
        raise WrongVariant("Out of choose. Input number from 1 to 3.")



if __name__ == "__main__":
    main()
