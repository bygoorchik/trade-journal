# загрузка сделок из excel

import pandas as pd


def load_trades(file):
    trades = pd.read_excel(file, sheet_name="Сделки")
    companies = pd.read_excel(file, sheet_name="Справочник")

    trades = trades.dropna(subset=["Тикер"])  # убираем пустые строки
    trades = trades.merge(companies, on="Тикер", how="left")  # добавляем название компании по тикеру
    return trades


# делим сделки на закрытые (уже продали) и открытые (еще держим)
def split_positions(trades):
    closed = trades.dropna(subset=["Дата продажи"]).copy()
    open_positions = trades[trades["Дата продажи"].isna()].copy()
    return closed, open_positions
