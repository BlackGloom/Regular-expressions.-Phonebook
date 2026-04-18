from pprint import pprint
import re

# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код

phone_pattern = r"(\+7|8)?\s*\(*(\d{3})\)*[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s*\(?доб\.?\s*(\d+)\)?)?"

header = contacts_list[0]
contacts_dict = {}

for row in contacts_list[1:]:
    if not row:
        continue
    full_name = " ".join(row[:3]).split()
    while len(full_name) < 3:
        full_name.append("")
    lastname, firstname, surname = full_name
    phone = row[5]
    if phone:
        match = re.search(phone_pattern, phone)
        if match:
            formatted_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
            if match.group(7):
                formatted_phone += f" доб.{match.group(7)}"
            phone = formatted_phone

    new_row = [lastname, firstname, surname, row[3], row[4], phone, row[6]]

    found = False
    for key in contacts_dict.keys():
        if lastname == key[0] and firstname == key[1]:
            if surname == key[2] or not key[2] or not surname:
                for i in range(len(new_row)):
                    if not contacts_dict[key][i] and new_row[i]:
                        contacts_dict[key][i] = new_row[i]
                found = True
                break

    if not found:
        contacts_dict[(lastname, firstname, surname)] = new_row

result_list = [header] + list(contacts_dict.values())


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook_fixed.csv", "w", encoding="utf-8", newline="") as f:
  writer = csv.writer(f)
  # Вместо contacts_list подставьте свой список
  writer.writerows(result_list)
print(f"Готово! В файле {len(result_list)} строк (включая заголовок).")