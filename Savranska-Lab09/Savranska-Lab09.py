import requests                            # підключаємо requests для HTTP-запитів до API НБУ
import pandas as pd                        # підключаємо pandas для роботи з даними
import matplotlib
matplotlib.use('Agg')                      # використовуємо бекенд без графічного вікна
import matplotlib.pyplot as plt            # підключаємо matplotlib для побудови графіка
import matplotlib.dates as mdates          # підключаємо форматування дат на осі X
import mplcursors                          # підключаємо mplcursors для інтерактивних підказок
import os                                  # підключаємо os для відкриття файлу

student_name = "Савранська Єва"            # змінна з прізвищем студента
student_group = "231"                      # змінна з номером групи

print("=" * 55)                            # виводимо роздільник
print(f" Студент: {student_name} | Група: {student_group}")  # виводимо інформацію про студента
print("=" * 55)                            # ще один роздільник

# --- Функція для отримання даних з API НБУ ---

def fetch_nbu_rates(currency: str, start: str, end: str) -> pd.DataFrame:
    """Отримує курс валюти з API Національного банку України"""  # опис функції
    url = (                                # формуємо URL запиту до API НБУ
        f"https://bank.gov.ua/NBU_Exchange/exchange_site"
        f"?start={start}&end={end}&valcode={currency}&sort=exchangedate&order=asc&json"
    )
    response = requests.get(url, timeout=15)       # виконуємо GET-запит з таймаутом 15 секунд
    response.raise_for_status()                    # викидаємо помилку якщо статус не 200
    data = response.json()                         # парсимо відповідь як JSON
    df = pd.DataFrame(data)                        # створюємо DataFrame з отриманих даних
    df["exchangedate"] = pd.to_datetime(           # перетворюємо рядок дати у формат datetime
        df["exchangedate"], format="%d.%m.%Y"
    )
    df = df[["exchangedate", "rate"]].rename(      # залишаємо тільки потрібні стовпці
        columns={"exchangedate": "date", "rate": currency}  # перейменовуємо стовпці
    )
    return df                                      # повертаємо готовий DataFrame

# --- Отримання даних ---

START = "20220101"                         # дата початку періоду: 01.01.2022
END   = pd.Timestamp.today().strftime("%Y%m%d")  # дата кінця: сьогодні

print(f"\n⏳ Завантаження даних з API НБУ...")     # повідомлення про початок завантаження
print(f"   Період: 01.01.2022 — {pd.Timestamp.today().strftime('%d.%m.%Y')}")  # виводимо період

df_usd = fetch_nbu_rates("USD", START, END)        # отримуємо курс USD
print(f"   ✅ USD: {len(df_usd)} записів")         # виводимо кількість записів USD

df_eur = fetch_nbu_rates("EUR", START, END)        # отримуємо курс EUR
print(f"   ✅ EUR: {len(df_eur)} записів")         # виводимо кількість записів EUR

# --- Об'єднання даних ---

df = pd.merge(df_usd, df_eur, on="date", how="inner")  # об'єднуємо таблиці по даті
df = df.set_index("date")                              # встановлюємо дату як індекс

print(f"\n📋 Останні 5 записів:")                  # заголовок таблиці
print(df.tail())                                   # виводимо останні 5 рядків

# --- Побудова графіка ---

fig, ax = plt.subplots(figsize=(14, 6))            # створюємо фігуру розміром 14×6 дюймів

line_usd, = ax.plot(                               # будуємо лінію курсу USD
    df.index, df["USD"],
    color="#1565C0",                               # темно-синій колір як на сайті НБУ
    linewidth=1.8,                                 # товщина лінії
    label="USD / UAH"                              # підпис для легенди
)

line_eur, = ax.plot(                               # будуємо лінію курсу EUR
    df.index, df["EUR"],
    color="#E53935",                               # червоний колір як на сайті НБУ
    linewidth=1.8,                                 # товщина лінії
    label="EUR / UAH"                              # підпис для легенди
)

# --- Заливка під лініями ---

ax.fill_between(df.index, df["USD"],               # заливаємо область під лінією USD
                alpha=0.08, color="#1565C0")       # напівпрозора синя заливка
ax.fill_between(df.index, df["EUR"],               # заливаємо область під лінією EUR
                alpha=0.08, color="#E53935")       # напівпрозора червона заливка

# --- Форматування осей ---

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))   # мітки кожні 3 місяці
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))   # формат: "Jan 2022"
plt.xticks(rotation=45, ha="right")               # повертаємо підписи на 45 градусів

ax.yaxis.set_major_formatter(                      # форматуємо числа на осі Y
    plt.FuncFormatter(lambda x, _: f"{x:.2f} ₴")  # додаємо знак гривні
)

ax.set_title(                                      # заголовок графіка
    f"Курс валют НБУ: USD та EUR до UAH | {student_name} | Група {student_group}\n"
    f"Період: 01.01.2022 — {pd.Timestamp.today().strftime('%d.%m.%Y')}",
    fontsize=13, pad=15
)
ax.set_xlabel("Дата", fontsize=11)                 # підпис осі X
ax.set_ylabel("Курс (грн)", fontsize=11)           # підпис осі Y
ax.legend(fontsize=11)                             # відображаємо легенду
ax.grid(True, alpha=0.25, linestyle="--")          # додаємо пунктирну сітку

# --- Інтерактивні підказки при наведенні ---

cursor = mplcursors.cursor(                        # створюємо інтерактивний курсор
    [line_usd, line_eur], hover=True               # відстежуємо обидві лінії при наведенні
)

@cursor.connect("add")                             # обробник події появи підказки
def on_add(sel):                                   # функція що викликається при наведенні
    idx = sel.index                                # отримуємо індекс найближчої точки
    date = df.index[idx]                           # отримуємо дату точки
    label = sel.artist.get_label()                 # отримуємо назву лінії (USD або EUR)
    currency = "USD" if "USD" in label else "EUR"  # визначаємо валюту
    rate = df[currency].iloc[idx]                  # отримуємо курс у цій точці
    sel.annotation.set_text(                       # встановлюємо текст підказки
        f"{label}\n"
        f"Дата: {date.strftime('%d.%m.%Y')}\n"
        f"Курс: {rate:.4f} ₴"
    )
    sel.annotation.get_bbox_patch().set(           # стилізуємо фон підказки
        facecolor="white", alpha=0.9, edgecolor="#cccccc"
    )

plt.tight_layout()                                 # автоматично підганяємо розміри
plt.savefig("exchange_rates.png", dpi=150)         # зберігаємо графік у файл PNG
print("\n✅ Графік збережено: exchange_rates.png")  # повідомлення про збереження
os.startfile("exchange_rates.png")                 # відкриваємо файл у переглядачі Windows
print("=" * 55)                                    # фінальний роздільник