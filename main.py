# главный файл, отсюда запускается вся программа

import os
import shutil
import subprocess
import sys
from pathlib import Path

from app.loader import load_trades, split_positions
from app.metrics import add_trade_columns, summary, by_company
from app.charts import equity_chart
from app.report import write_report

JOURNAL = Path("data/journal.xlsx")  # наш журнал со сделками
TEMPLATE = Path("data/journal_template.xlsx")  # шаблон
OUTPUT = Path("output")  # сюда сохраняется отчет и график
REPORT = OUTPUT / "report.xlsx"
CHART = OUTPUT / "equity.png"


# открываем файл в программе по умолчанию (на windows и linux по разному)
def open_file(path):
    try:
        if sys.platform == "win32":
            os.startfile(path)
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        print("Не получилось открыть отчет сам, откройте его вручную:", path)


def main():
    # если журнала нет то копируем шаблон
    if not JOURNAL.exists():
        shutil.copy(TEMPLATE, JOURNAL)
        print("Создан", JOURNAL, "из шаблона, заполните его своими сделками")

    OUTPUT.mkdir(exist_ok=True)

    # 1 - читаем сделки
    trades = load_trades(JOURNAL)
    closed, open_positions = split_positions(trades)

    # 2 - считаем
    closed = add_trade_columns(closed)
    metrics = summary(trades, closed, open_positions)

    # 3 - рисуем график
    equity_chart(closed, CHART)

    # 4 - сохраняем отчет
    try:
        write_report(REPORT, {
            "Статистика": metrics,
            "По компаниям": by_company(closed),
            "Расчёт": closed,
            "Открытые позиции": open_positions,
        }, CHART)
    except PermissionError:
        print("Ошибка: закройте файл", REPORT, "и запустите программу еще раз")
        return

    print(metrics.to_string(index=False))
    print("\nГотово! Отчет сохранен в", REPORT)
    open_file(REPORT)


if __name__ == "__main__":
    main()
