import csv
import re
from pprint import pprint
from collections import defaultdict

# Чтение исходного файла и преобразование в список
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Коррекция ФИО
def correct_fio(contact):
    full_name = " ".join(contact[:3]).split()
    while len(full_name) < 3:
        full_name.append("")
    contact[:3] = full_name
    return contact

contacts_list = [correct_fio(contact) for contact in contacts_list]

# Форматирование телефона
def format_phone(phone):
    pattern = re.compile(r"(\+7|8)?\s*\(?(\d{3})\)?\s*-?\s*(\d{3})\s*-?\s*(\d{2})\s*-?\s*(\d{2})(\s*\(?(доб\.)\s*(\d+)\)?)?")
    formatted_phone = pattern.sub(r"+7(\2)\3-\4-\5 \7\8", phone).strip()
    return formatted_phone

for contact in contacts_list:
    contact[5] = format_phone(contact[5])

# Объединение дублирующихся записей
def merge_contacts(contacts):
    merged_contacts = defaultdict(lambda: ["", "", "", "", "", "", ""])
    for contact in contacts:
        key = (contact[0], contact[1])
        for i, field in enumerate(contact):
            if field:
                merged_contacts[key][i] = field
    return list(merged_contacts.values())

contacts_list = merge_contacts(contacts_list)

# Запись обновленных данных в новый файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)
