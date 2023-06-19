from src.orders import process_orders
from src.arbitrage import process_arbitrage



class InvalidInput(ValueError):
    pass

class WrongVariant(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def main():
    print("It's time to choose!\n1 - orders only;\n2 - arbitrage only\n3 - both;")

    try:
        user_req = int(input())
        print("Yes, Boss! Processing.")
    except ValueError:
        raise InvalidInput("Not a number. Input number from 1 to 3.")

    if user_req == 1:
        process_orders()
    elif user_req == 2:
        process_arbitrage()
    elif user_req == 3:
        process_orders()
        process_arbitrage()
    else:
        raise WrongVariant("Out of choose. Input number from 1 to 3.")



if __name__ == "__main__":
    main()
