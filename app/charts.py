# график капитала

import matplotlib
matplotlib.use("Agg")  # чтобы график сохранялся в файл а не открывался в окне
import matplotlib.pyplot as plt

# цвета
ORANGE = "#FF8C1A"
BACKGROUND = "#141414"
TEXT = "#E6E6E6"


def equity_chart(closed, path):
    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BACKGROUND)

    # линия прибыли по датам продаж
    ax.plot(closed["Дата продажи"], closed["Накопленная прибыль, ₽"],
            color=ORANGE, linewidth=2.5, marker="o")
    ax.axhline(0, color=TEXT, linewidth=0.8, alpha=0.4)  # линия нуля

    ax.set_title("Кривая капитала", color=TEXT, fontsize=14, loc="left")
    ax.set_ylabel("Прибыль, ₽", color=TEXT)
    ax.set_facecolor(BACKGROUND)
    ax.tick_params(colors=TEXT)
    ax.grid(alpha=0.15)
    for side in ax.spines.values():  # убираем рамку
        side.set_visible(False)

    fig.autofmt_xdate()  # даты наискосок чтобы не налезали
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
