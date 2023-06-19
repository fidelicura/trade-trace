# импорт библиотек
import logging
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment
from datetime import datetime, timedelta
from binance.error import ClientError
from binance.lib.utils import config_logging
from binance.spot import Spot as Client
from openpyxl.styles.numbers import BUILTIN_FORMATS as cellFormat
# импорт библиотек

# основная часть кода
time_now = datetime.now().strftime("%Y.%m.%d")
time_ago = (datetime.now() - timedelta(weeks=4)).strftime("%Y.%m.%d")
config_logging(logging, logging.DEBUG)
api_key = input(str("Укажите ваш API-ключ: "))
secret_key = input(str("Укажите ваш секретный ключ: "))
client = Client(api_key, secret_key)
try:
    response = client.c2c_trade_history("BUY")
    df = pd.json_normalize(response, "data")
    df["createTime"] = (df["createTime"] / 1000).astype(int)
    df["createTime"] = pd.to_datetime(df["createTime"], unit="s")
    df["totalPrice"] = round(df["totalPrice"].astype(float), 2).replace(".", ",")
    df["unitPrice"] = df["unitPrice"].astype(float) + (df["unitPrice"].astype(float) / 100 * 0.1)
    df["amount"] = df["amount"].astype(float) - (df["amount"].astype(float) / 100 * 0.1)
    df.drop(df.loc[df["orderStatus"] != "COMPLETED"].index, inplace=True)
    df["orderStatus"] = df["orderStatus"].str.replace("COMPLETED", "Завершён")
    df.rename(columns={
        "orderNumber": "Ордер",
        "orderStatus": "Статус ордера",
        "createTime": "Время",
        "amount": "USDT",
        "totalPrice": "UAH",
        "unitPrice": "Курс"
    }, inplace=True)
    df.drop(columns=[
        "advertisementRole",
        "fiatSymbol",
        "counterPartNickName",
        "commission",
        "tradeType",
        "asset",
        "fiat",
        "advNo"
    ]).to_excel(
        "Результат.xlsx",
        sheet_name=f"{time_ago} - {time_now}",
        index="False"
    )
    book = openpyxl.load_workbook(filename="Результат.xlsx")
    sheet = book.active
    sheet.column_dimensions["B"].width = 23
    sheet.column_dimensions["C"].width = 23
    sheet.column_dimensions["D"].width = 23
    sheet.column_dimensions["E"].width = 23
    sheet.column_dimensions["F"].width = 23
    sheet.column_dimensions["G"].width = 23
    letter_list_cells = ["B", "C", "D", "E", "F", "G"]
    for letter in letter_list_cells:
        for i in range(1, int(len(df.index)) + 2):
            sheet[f"{letter}{i}"].alignment = Alignment(horizontal="center")
    letter_list_cells_numbers = ["C", "D", "E"]
    for letter in letter_list_cells_numbers:
        for i in range(1, int(len(df.index)) + 2):
            sheet[f"{letter}{i}"].number_format = cellFormat[2]
    book.save("Результат.xlsx")
    average_exchange_rate = df["Курс"].mean()
    usdt_month = df["USDT"].astype(float).sum()
    uah_month = df["UAH"].astype(float).sum()
    with open("Статистика за месяц.txt", "w+") as stats_file:
        stats_file.write(
            "Всего потрачено UAH за месяц: {} грн\nВсего получено USDT за месяц: {} $\nИтоговый курс за месяц: {}".format(round(uah_month, 2), round(usdt_month, 2), round(average_exchange_rate, 2)))
    print("Успех! Ваш файл был загружен!")
    input("Нажмите Enter для выхода из программы...")
except ClientError as error:
    logging.error(f"Найдена ошибка. Статус: {error.status_code}, Код: {error.error_code}, Сообщение: {error.error_message}")
# основная часть кода
