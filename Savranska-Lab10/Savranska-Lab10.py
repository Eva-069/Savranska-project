import pandas as pd                        # підключаємо pandas — єдина дозволена бібліотека

student_name = "Савранська Єва"            # змінна з прізвищем студента
student_group = "231"                      # змінна з номером групи
last_name = "Savranska"                    # прізвище латиницею для назв файлів

print("=" * 50)                            # виводимо роздільник
print(f" Студент: {student_name} | Група: {student_group}")  # виводимо інформацію про студента
print("=" * 50)                            # ще один роздільник

# --- Крок 1: Зчитуємо Excel файл ---

df = pd.read_excel("data.xlsx")            # зчитуємо Excel файл у DataFrame
print(f"\n📋 Вихідна таблиця ({len(df)} рядків):")  # виводимо кількість рядків
print(df.to_string(index=False))           # виводимо всю таблицю без індексів

# --- Крок 2: Прибираємо неповні рядки ---

df_clean = df.dropna()                     # видаляємо рядки де є хоча б одне пусте значення
df_clean = df_clean.reset_index(drop=True) # скидаємо індекси після видалення рядків

print(f"\n🧹 Після видалення неповних рядків ({len(df_clean)} рядків):")  # виводимо нову кількість
print(df_clean.to_string(index=False))     # виводимо очищену таблицю

# --- Крок 3: Зберігаємо у три формати ---

csv_file  = f"{last_name}.csv"             # назва CSV файлу
json_file = f"{last_name}.json"            # назва JSON файлу
xml_file  = f"{last_name}.xml"             # назва XML файлу

df_clean.to_csv(csv_file, index=False, encoding="utf-8")           # зберігаємо як CSV
df_clean.to_json(json_file, orient="records", indent=2, force_ascii=False)  # зберігаємо як JSON
df_clean.to_xml(xml_file, index=False)     # зберігаємо як XML

print(f"\n✅ Файли збережено:")             # виводимо список збережених файлів
print(f"   📄 {csv_file}")                 # виводимо назву CSV файлу
print(f"   📄 {json_file}")                # виводимо назву JSON файлу
print(f"   📄 {xml_file}")                 # виводимо назву XML файлу

# --- Крок 4: Статистика по полю age ---

age = df_clean["age"]                      # виділяємо стовпець age для розрахунків

avg_age = round(age.mean(), 2)             # середній вік: сума / кількість
min_age = int(age.min())                   # мінімальний вік
max_age = int(age.max())                   # максимальний вік

print(f"\n📊 Статистика по полю age:")      # заголовок блоку статистики
print(f"   Середній вік (avg): {avg_age}") # виводимо середній вік
print(f"   Мінімальний вік (min): {min_age}")  # виводимо мінімальний вік
print(f"   Максимальний вік (max): {max_age}") # виводимо максимальний вік

print("\n" + "=" * 50)                     # фінальний роздільник