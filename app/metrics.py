# здесь все расчеты

import pandas as pd


# добавляем новые столбцы для каждой сделки
def add_trade_columns(closed):
    closed["Вложено, ₽"] = closed["Цена покупки, ₽"] * closed["Количество, шт"]
    closed["Прибыль, ₽"] = (closed["Цена продажи, ₽"] - closed["Цена покупки, ₽"]) * closed["Количество, шт"]
    closed["Доходность, %"] = (closed["Цена продажи, ₽"] / closed["Цена покупки, ₽"] - 1) * 100
    closed["Дней в позиции"] = (closed["Дата продажи"] - closed["Дата покупки"]).dt.days

    # сортируем по дате продажи и считаем прибыль нарастающим итогом
    closed = closed.sort_values("Дата продажи")
    closed["Накопленная прибыль, ₽"] = closed["Прибыль, ₽"].cumsum()

    # просадка - насколько упали от самого лучшего результата
    closed["Просадка, ₽"] = closed["Накопленная прибыль, ₽"].cummax().clip(lower=0) - closed["Накопленная прибыль, ₽"]
    return closed


# общая статистика
def summary(trades, closed, open_positions):
    wins = closed[closed["Прибыль, ₽"] > 0]  # сделки в плюс
    losses = closed[closed["Прибыль, ₽"] < 0]  # сделки в минус
    period = f'{trades["Дата покупки"].min():%d.%m.%Y} — {closed["Дата продажи"].max():%d.%m.%Y}'

    return pd.DataFrame({
        "Метрика": ["Период", "Закрытых сделок", "Открытых позиций", "Winrate, %",
                    "Итоговая прибыль, ₽", "Доходность к вложенному, %", "Средняя доходность сделки, %",
                    "Средний срок владения, дней", "Profit factor", "Максимальная просадка, ₽"],
        "Значение": [period,
                     len(closed),
                     len(open_positions),
                     round(len(wins) / len(closed) * 100, 1),
                     round(closed["Прибыль, ₽"].sum(), 2),
                     round(closed["Прибыль, ₽"].sum() / closed["Вложено, ₽"].sum() * 100, 2),
                     round(closed["Доходность, %"].mean(), 2),
                     round(closed["Дней в позиции"].mean()),
                     round(wins["Прибыль, ₽"].sum() / abs(losses["Прибыль, ₽"].sum()), 2),
                     round(closed["Просадка, ₽"].max(), 2)],
    })


# статистика по каждой компании отдельно
def by_company(closed):
    return closed.groupby(["Тикер", "Компания"]).agg(
        Сделок=("Прибыль, ₽", "count"),
        Прибыль=("Прибыль, ₽", "sum"),
        Средняя_доходность=("Доходность, %", "mean"),
        Средний_срок=("Дней в позиции", "mean"),
    ).round(2).sort_values("Прибыль", ascending=False).reset_index()
