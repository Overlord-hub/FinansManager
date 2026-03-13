import json
import os

# Назва файлу для зберігання даних
DATA_FILE = "finance_data.json"


def load_data():
    """Завантажує дані з JSON файлу або створює нову структуру, якщо файл відсутній."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"budget": 0.0, "expenses": []}


def save_data(data):
    """Зберігає поточні дані у JSON файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def set_budget(data):
    """Встановлює загальний бюджет користувача."""
    try:
        amount = float(input("Введіть суму бюджету: "))
        data["budget"] = amount
        save_data(data)
        print(f"Бюджет успішно встановлено: {amount}")
    except ValueError:
        print("Помилка: введіть числове значення.")


def add_expense(data):
    """Додає нову витрату та перевіряє ліміт бюджету."""
    try:
        amount = float(input("Введіть суму витрати: "))
        category = input("Введіть категорію (напр., Їжа, Транспорт): ")
        date = input("Введіть дату (РРРР-ММ-ДД): ")
        comment = input("Коментар (необов'язково): ")

        expense = {
            "amount": amount,
            "category": category,
            "date": date,
            "comment": comment
        }

        data["expenses"].append(expense)
        save_data(data)
        print("Витрату додано!")

        # ПЕРЕВІРКА БЮДЖЕТУ
        total_spent = sum(e["amount"] for e in data["expenses"])
        if total_spent > data["budget"]:
            diff = total_spent - data["budget"]
            # Тут я прибрав складний вираз з f-рядка, щоб не було конфлікту лапок
            print(f"⚠️ ПОПЕРЕДЖЕННЯ: Ви перевищили бюджет на {diff:.2f}!")

    except ValueError:
        print("Помилка: сума має бути числом.")


def show_expenses(expenses_list):
    """Виводить список витрат у зручному форматі."""
    if not expenses_list:
        print("Список витрат порожній.")
        return

    print("\n--- Список витрат ---")
    for i, exp in enumerate(expenses_list, 1):
        print(f"{i}. {exp['date']} | {exp['category']}: {exp['amount']} грн ({exp['comment']})")


def show_balance(data):
    """Рахує та виводить залишок бюджету."""
    total_spent = sum(e["amount"] for e in data["expenses"])
    balance = data["budget"] - total_spent
    print(f"\nЗагальний бюджет: {data['budget']}")
    print(f"Витрачено: {total_spent}")
    print(f"Залишок: {balance}")


def category_report(data):
    """Звіт за категоріями."""
    report = {}
    for exp in data["expenses"]:
        cat = exp["category"]
        report[cat] = report.get(cat, 0) + exp["amount"]

    print("\n--- Звіт за категоріями ---")
    for cat, total in report.items():
        print(f"{cat}: {total} грн")


def filter_expenses(data):
    """Підменю для фільтрації витрат."""
    print("\n1. За конкретну дату\n2. За категорією\n3. Назад")
    choice = input("Оберіть варіант фільтрації: ")

    if choice == "1":
        date = input("Введіть дату (РРРР-ММ-ДД): ")
        filtered = [e for e in data["expenses"] if e["date"] == date]
        show_expenses(filtered)
    elif choice == "2":
        cat = input("Введіть назву категорії: ")
        filtered = [e for e in data["expenses"] if e["category"].lower() == cat.lower()]
        show_expenses(filtered)


def main():
    """Основний цикл роботи бота."""
    data = load_data()
    print("Вітаємо у 'Фінансовому трекері студента'!")

    while True:
        print(
            "\nДоступні команди: допомога, встановити бюджет, додати витрату, показати витрати, фільтри, залишок, звіт, вийти")
        command = input("Введіть команду: ").lower().strip()

        if command == "допомога":
            print("\nДовідка за командами:")
            print("- встановити бюджет: задати ліміт грошей")
            print("- додати витрату: записати нову покупку")
            print("- показати витрати: переглянути весь список")
            print("- фільтри: пошук за датою або категорією")
            print("- залишок: перевірити баланс")
            print("- звіт: суми за категоріями")
            print("- вийти: закрити програму")

        elif command == "встановити бюджет":
            set_budget(data)
        elif command == "додати витрату":
            add_expense(data)
        elif command == "показати витрати":
            show_expenses(data["expenses"])
        elif command == "фільтри":
            filter_expenses(data)
        elif command == "залишок":
            show_balance(data)
        elif command == "звіт":
            category_report(data)
        elif command == "вийти":
            print("До побачення! Успіхів у плануванні бюджету.")
            break
        else:
            print("Невідома команда. Спробуйте ще раз або введіть 'допомога'.")


if __name__ == "__main__":
    main()