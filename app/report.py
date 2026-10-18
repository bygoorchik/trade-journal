# сохраняем отчет в отдельный excel файл

import pandas as pd
from openpyxl.drawing.image import Image


def write_report(file, tables, chart_path):
    with pd.ExcelWriter(file, engine="openpyxl") as writer:
        # каждая таблица на свой лист
        for sheet_name, table in tables.items():
            table.to_excel(writer, sheet_name=sheet_name, index=False)

        # делаем столбцы шире
        for sheet in writer.book.worksheets:
            for col in sheet.columns:
                sheet.column_dimensions[col[0].column_letter].width = 24

        # лист с картинкой графика
        chart_sheet = writer.book.create_sheet("График")
        chart_sheet.add_image(Image(chart_path), "A1")
