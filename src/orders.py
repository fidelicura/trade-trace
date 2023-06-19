import pandas as pd
import openpyxl as opyx
from openpyxl.styles import Alignment
from openpyxl.workbook import Workbook
from openpyxl.styles.numbers import BUILTIN_FORMATS as cellFormat
from binance.error import ClientError
from binance.spot import Spot as Client
# from binance.lib.utils import config_logging
from src.general import calculate_time_delta, logger
from datetime import datetime



def parse_json(client: Client) -> pd.DataFrame:
    dfs = []
    for trade_type in ("BUY", "SELL"):
        response = client.c2c_trade_history(trade_type)
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

    df.drop(df.loc[df["orderStatus"] != "COMPLETED"].index, inplace=True)

    return df

def rename_table(df) -> pd.DataFrame:
    df.rename(columns={
        "orderNumber": "Order Number",
        "orderStatus": "Order Status",
        "createTime": "Time",
        "amount": "Sold Currency",
        "totalPrice": "Bought Currency",
        "unitPrice": "Exchange Rate"
    }, inplace=True)

    return df

def drop_unused(df) -> pd.DataFrame:
    df.drop(columns=[
        "advertisementRole",
        "fiatSymbol",
        "counterPartNickName",
        "commission",
        "tradeType",
        "asset",
        "fiat",
        "advNo"
    ])

    return df

def table_to_excel(df: pd.DataFrame, start: datetime, end: datetime) -> str:
    file_name = "orders.xlsx"
    sheet_name = f"{start} - {end}"

    df.to_excel(file_name, sheet_name, False)

    return file_name


def load_sheet(file_name: str) -> Workbook:
    book = opyx.load_workbook(filename="result.xlsx")
    sheet = book.active

    return sheet

def prettify_sheet(sheet: Workbook):
    for dim in ("B", "C", "D", "E", "F", "G"):
        sheet.column_dimensions[dim] = 23

    for num in range(1, len(sheet.rows) + 1):
        for letter in ("B", "C", "D", "E", "F", "G"):
            sheet[f"{letter}{num}"].alignment = Alignment(horizontal="center")

            if letter in ("C", "D", "E"):
                sheet[f"{letter}{i}"].number_format = cellFormat[2]
    
    try:
        book.save("orders.xlsx")
        print("Result spreadsheet is ready!")
    except Exception as err:
        logging.info("unable to save results to output xlsx")
        raise err 




def process_orders():
    client = Client(api_key, secret_key)
    (start, end) = calculate_time_delta()

    raw_pd = parse_json(client)
    raw_table = create_table(raw_pd)
    not_pretty_table = rename_table(raw_table)
    almost_pretty_table = drop_unused(not_pretty_table)
    raw_output = table_to_excel(almost_pretty_table, start, end)

    loaded_raw = load_sheet(raw_output)
    pretty_table = prettify_sheet(loaded_raw)
