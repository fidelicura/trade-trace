import os
import pandas as pd
import openpyxl as opyx
from openpyxl.styles import Alignment
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles.numbers import BUILTIN_FORMATS as cellFormat
from binance.error import ClientError
from binance.spot import Spot as Client
from src.general import calculate_time_delta, logger, read_keys
from datetime import datetime
from typing import Tuple



def parse_json(client: Client) -> pd.DataFrame:
    dfs = []
    for trade_type in ("BUY", "SELL"):
        response = client.c2c_trade_history(tradeType=trade_type)
        df = pd.json_normalize(response, "data")
        dfs.append(df)

    result = pd.concat(dfs, ignore_index=True)
    return result


def create_table(df) -> pd.DataFrame:
    df["createTime"] = (df["createTime"] / 1000).astype(int)
    df["createTime"] = pd.to_datetime(df["createTime"], unit="s")

    df["totalPrice"] = round(df["totalPrice"].astype(float), 2).replace(".", ",")
    df["unitPrice"] = df["unitPrice"].astype(float) + (df["unitPrice"].astype(float) / 100 * 0.1)

    df["amount"] = df["amount"].astype(float) - (df["amount"].astype(float) / 100 * 0.1)

    user_choice = str(input("Write completed orders only? (y/n): "))
    if user_choice == "y":
        df.drop(df.loc[df["orderStatus"] != "COMPLETED"].index, inplace=True)
    elif user_choice == "n":
        pass
    else:
        raise ValueError("Invalid input. We have only completed and uncompleted orders, so `y` or `n`")

    return df

def rename_table(df):
    df.rename(columns={
        "orderNumber": "Order Number",
        "tradeType": "Trade Type",
        "orderStatus": "Order Status",
        "createTime": "Time",
        "amount": "Sold Currency",
        "totalPrice": "Bought Currency",
        "unitPrice": "Exchange Rate"
    }, inplace=True)

def drop_unused(df):
    df.drop(columns=[
        "advertisementRole",
        "fiatSymbol",
        "counterPartNickName",
        "commission",
        "asset",
        "fiat",
        "advNo"
    ], inplace=True)

def table_to_excel(df: pd.DataFrame, start: datetime, end: datetime) -> str:
    folder_name = "output"
    sheet_name = f"{start} - {end}"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_name = "output/orders.xlsx"
    df.to_excel(file_name, sheet_name, False)

    return file_name


def load_sheet(file_name: str) -> Worksheet:
    book = opyx.load_workbook(filename="output/orders.xlsx")
    sheet = book.active

    return sheet

def prettify_sheet(sheet: Worksheet):
    for dim in ("B", "C", "D", "E", "F", "G", "H"):
        sheet.column_dimensions[dim].width = 23

    for num in range(1, sheet.max_row + 1):
        for letter in ("B", "C", "D", "E", "F", "G", "H"):
            sheet[f"{letter}{num}"].alignment = Alignment(horizontal="center")

            if letter in ("D", "E", "F"):
                sheet[f"{letter}{num}"].number_format = cellFormat[2]
    
    try:
        sheet.parent.save("output/orders.xlsx")
        print("Result spreadsheet is ready!")
        print("It contains orders about last 30 days.")
        print("No way to make bigger timestamp due to Binance restrictions.")
        print("Thanks for understanding.")
        print("Closing program, thanks for your usage!")
    except Exception as err:
        logger.info("unable to save results to output xlsx")
        raise err 



def process_orders(client: Client):
    start, end = calculate_time_delta()

    raw_pd = parse_json(client)
    raw_table = create_table(raw_pd)
    rename_table(raw_table)
    drop_unused(raw_table)
    raw_output = table_to_excel(raw_table, start, end)

    raw_sheet = load_sheet(raw_output)
    prettify_sheet(raw_sheet)
