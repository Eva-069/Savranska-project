import pandas as pd                        # підключаємо pandas для роботи з таблицями
import matplotlib.pyplot as plt            # підключаємо matplotlib для побудови графіків
import matplotlib.ticker as mticker        # підключаємо форматування осей matplotlib
import seaborn as sns                      # підключаємо seaborn для стилізованих графіків

student_name = "Савранська Єва"            # змінна з прізвищем студента
student_group = "231"                      # змінна з номером групи

print("=" * 50)                            # виводимо роздільник
print(f" Студент: {student_name} | Група: {student_group}")  # виводимо інформацію про студента
print("=" * 50)                            # ще один роздільник

# --- Підготовка даних ---

df = pd.read_csv("sales.csv")              # зчитуємо CSV файл у DataFrame
df["date"] = pd.to_datetime(df["date"])    # перетворюємо стовпець date у формат дати
df["revenue"] = df["qty"] * df["price"]   # рахуємо виручку: кількість × ціна
df["month"] = df["date"].dt.to_period("M") # витягуємо місяць у форматі "2025-01"

monthly = df.groupby("month")["revenue"].sum().reset_index()  # групуємо по місяцю і сумуємо виручку
monthly["month_dt"] = monthly["month"].dt.to_timestamp()      # перетворюємо Period у datetime для графіка
monthly["rolling3"] = monthly["revenue"].rolling(3).mean()    # рахуємо 3-місячне ковзне середнє

print("\n📅 Помісячна виручка:")           # заголовок таблиці
print(monthly[["month", "revenue", "rolling3"]].to_string(index=False))  # виводимо таблицю без індексів

# --- Графік 1: Matplotlib ---

fig, ax = plt.subplots(figsize=(12, 5))   # створюємо фігуру розміром 12×5 дюймів

ax.plot(monthly["month_dt"], monthly["revenue"],    # будуємо лінію виручки по місяцях
        color="#2196F3", marker="o",                # синій колір з маркерами-крапками
        linewidth=2, label="Виручка")               # товщина лінії 2, підпис для легенди

ax.plot(monthly["month_dt"], monthly["rolling3"],   # будуємо лінію ковзного середнього
        color="#FF5722", linestyle="--",            # помаранчевий колір, пунктирна лінія
        linewidth=2, label="Ковзне середнє (3 міс)")  # підпис для легенди

peak_idx = monthly["revenue"].idxmax()              # знаходимо індекс місяця з максимальною виручкою
peak_x = monthly.loc[peak_idx, "month_dt"]         # отримуємо дату пікового місяця
peak_y = monthly.loc[peak_idx, "revenue"]          # отримуємо значення пікової виручки

ax.annotate(f"Пік: {peak_y:,.0f}",                 # підписуємо пікову точку текстом
            xy=(peak_x, peak_y),                   # координати стрілки (де точка)
            xytext=(peak_x, peak_y + 8000),        # координати тексту (трохи вище)
            arrowprops=dict(arrowstyle="->", color="black"),  # стиль стрілки
            fontsize=10, color="black")             # розмір і колір тексту

ax.set_title(f"Помісячна виручка | {student_name} | Група {student_group}",
             fontsize=13)                           # заголовок графіка з іменем студента
ax.set_xlabel("Місяць")                            # підпис осі X
ax.set_ylabel("Виручка (грн)")                     # підпис осі Y
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))  # форматуємо числа на осі Y
ax.legend()                                        # відображаємо легенду
ax.grid(True, alpha=0.3)                           # додаємо прозору сітку
plt.tight_layout()                                 # автоматично підганяємо розміри
plt.savefig("chart_matplotlib.png", dpi=150)       # зберігаємо графік у файл PNG
plt.show()                                         # відображаємо графік на екрані
print("\n✅ Matplotlib графік збережено: chart_matplotlib.png")  # повідомлення про збереження

# --- Графік 2: Seaborn ---

sns.set_theme(style="darkgrid", palette="muted")   # встановлюємо темну сітку і приглушену палітру

fig2, ax2 = plt.subplots(figsize=(12, 5))          # створюємо нову фігуру

sns.lineplot(data=monthly, x="month_dt",           # будуємо лінійний графік виручки
             y="revenue", ax=ax2,                  # вказуємо осі
             color="#1565C0", linewidth=2.5,        # синій колір, товста лінія
             marker="o", errorbar=None,             # маркери без довірчого інтервалу
             label="Виручка")                       # підпис для легенди

quarters = ["2025-01-01", "2025-04-01",            # дати початків кварталів
            "2025-07-01", "2025-10-01"]             # Q1, Q2, Q3, Q4

quarter_labels = ["Q1", "Q2", "Q3", "Q4"]          # підписи кварталів

for q_date, q_label in zip(quarters, quarter_labels):           # перебираємо дати і підписи кварталів
    ax2.axvline(pd.Timestamp(q_date),                           # малюємо вертикальну лінію
                color="red", linestyle=":", alpha=0.7,          # червона пунктирна напівпрозора
                linewidth=1.5)                                   # товщина лінії
    ax2.text(pd.Timestamp(q_date), monthly["revenue"].max() * 0.95,  # розміщуємо текст вгорі
             q_label, color="red", fontsize=9, ha="center")     # підпис кварталу червоним

ax2.set_title(f"Помісячна виручка (Seaborn) | {student_name} | Група {student_group}",
              fontsize=13)                          # заголовок графіка
ax2.set_xlabel("Місяць")                           # підпис осі X
ax2.set_ylabel("Виручка (грн)")                    # підпис осі Y
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))  # форматуємо числа на осі Y
ax2.legend()                                       # відображаємо легенду
plt.tight_layout()                                 # автоматично підганяємо розміри
plt.savefig("chart_seaborn.png", dpi=150)          # зберігаємо графік у файл PNG
plt.show()                                         # відображаємо графік на екрані
print("✅ Seaborn графік збережено: chart_seaborn.png")  # повідомлення про збереження
print("\n" + "=" * 50)                             # фінальний роздільник