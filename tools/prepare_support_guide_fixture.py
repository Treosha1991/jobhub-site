"""Normalize fictional user-entered labels in a local Support guide fixture.

This script only changes the SQLite file passed on the command line. It never
connects to staging or production and intentionally leaves UI translations to
the application.
"""

import argparse
import sqlite3
from pathlib import Path


REPLACEMENTS = {
    "auth_user": {
        "first_name": {
            "Алина": "Alina", "Игорь": "Igor", "Марина": "Marina",
            "Олег": "Oleg", "Наталья": "Natalia", "Артём": "Artem",
            "Виктория": "Victoria", "Денис": "Denis",
        },
        "last_name": {
            "Бондарь": "Bondar", "Коваль": "Koval", "Левченко": "Levchenko",
            "Савчук": "Savchuk", "Мельник": "Melnyk", "Романюк": "Romaniuk",
            "Ткаченко": "Tkachenko", "Шевченко": "Shevchenko",
        },
    },
    "support_workproject": {
        "internal_name": {"Демо-проект А": "Demo Project A"},
        "worker_visible_name": {"Демо-проект А": "Demo Project A"},
    },
    "support_worksite": {
        "internal_name": {"Демо-проект А": "Demo Project A"},
        "city": {"Демоград": "Demo City"},
        "street": {"Примерная улица": "Example Street"},
    },
    "support_projectcrew": {
        "internal_name": {"Демо-экипаж": "Demo Crew"},
    },
    "support_scheduledworkshift": {
        "worker_label": {"Демо-экипаж": "Demo Crew"},
    },
    "support_housingsite": {
        "internal_name": {"Демо-дом А": "Demo House A"},
        "city": {"Демоград": "Demo City"},
        "street": {"Образцовая улица": "Sample Street"},
    },
    "support_housingroom": {"label": {"Комната А": "Room A"}},
    "support_vehicle": {"internal_name": {"Демоавтобус": "Demo Minibus"}},
    "support_workertask": {
        "title": {"Проверить демо-отчёт": "Review the sample report"},
        "instructions": {
            "Откройте вымышленный отчёт и отметьте, что данные готовы к проверке.":
                "Open the fictional report and mark it ready for review."
        },
    },
    "support_workerrequest": {
        "worker_note": {"Прошу выходной в пятницу.": "I would like Friday off."}
    },
    "support_supportvacancy": {
        "internal_title": {"Демонстрация: склад в Нидерландах": "Demo: warehouse in the Netherlands"}
    },
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sqlite_file", type=Path)
    args = parser.parse_args()
    if not args.sqlite_file.is_file() or args.sqlite_file.name != "support-guide-demo.sqlite3":
        parser.error("pass the existing support-guide-demo.sqlite3 fixture")
    changed = 0
    with sqlite3.connect(args.sqlite_file) as db:
        for table, columns in REPLACEMENTS.items():
            for column, values in columns.items():
                for old, new in values.items():
                    cursor = db.execute(
                        f'UPDATE "{table}" SET "{column}" = ? WHERE "{column}" = ?',
                        (new, old),
                    )
                    changed += cursor.rowcount
        db.commit()
    print(f"Normalized {changed} fictional labels in {args.sqlite_file.name}")


if __name__ == "__main__":
    main()
