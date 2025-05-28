import csv
import os
from datetime import datetime

CSV_FILE = "expenses.csv"

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "amount", "category", "description", "date"])

def get_next_id():
    try:
        with open(CSV_FILE, mode='r') as file:
            rows = list(csv.reader(file))
            if len(rows) > 1:
                return int(rows[-1][0]) + 1
            else:
                return 1
    except:
        return 1

def add_expense():
    amount = input("Enter amount: ")
    category = input("Enter category (e.g. Food, Travel): ")
    description = input("Enter description: ")
    date = datetime.now().strftime("%Y-%m-%d")
    
    expense_id = get_next_id()

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([expense_id, amount, category, description, date])
    
    print("Expense added.")

CATEGORY_KEYWORDS = {
    "FOODBOOK": "food",
    "PAYTM": "food",
    "RECHARGE": "recharge",
    "GOOGLE": "recharge",
    "KSRTC": "travel",
    "MAKEMYTRIP": "travel",
    "MEDIC": "medicals",
    "HOSPITAL": "medicals",
    "HOSTELLER": "stay",
    "BESCOM": "bill",
    "EMI": "emi",
    "CLOTHES": "clothes",
    "MYNTRA": "clothes",
    "HONDA": "service",
    "MART": "groceries",
    "COMPASS": "food",
    "COURSERA": "certificate",
    "SMOKE": "smokes",
    "ABDUL": "smokes",
    "SURAJ": "smokes"
}

def import_bank_csv(bank_csv_file):
    with open(bank_csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            amount = row["Withdrawal Amt."].strip()
            if amount:
                description = row["Narration"].strip()
                date = row["Date"].strip()

                # Auto-categorization
                category = None
                for keyword, cat in CATEGORY_KEYWORDS.items():
                    if keyword.lower() in description.lower():
                        category = cat
                        break

                if not category:
                    try:
                        if 73 <= float(amount) <= 77:
                            category = "smokes"
                    except ValueError:
                        pass

                if not category:
                    category = input(f"Enter category for: {description[:40]}... | ₹{amount}: ")
                else:
                    print(f"Auto-categorized '{description[:30]}...' as '{category}'")

                expense_id = get_next_id()

                with open(CSV_FILE, mode='a', newline='') as out_file:
                    writer = csv.writer(out_file)
                    writer.writerow([expense_id, amount, category, description, date])

    print("Import complete.")

def view_totals_by_category():
    totals = {}
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cat = row["category"]
                try:
                    amount = float(row["amount"])
                except ValueError:
                    print(f"Skipping invalid amount: {row['amount']} (ID: {row.get('id')})")
                    continue

                if cat in totals:
                    totals[cat] += amount
                else:
                    totals[cat] = amount
    except FileNotFoundError:
        print("No expense file found.")
        return

    print("\n=== Total Spent by Category ===")
    for cat, amt in totals.items():
        print(f"{cat:<15}: ₹{amt:.2f}")



def edit_category():
    # Load all data
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
    except FileNotFoundError:
        print("Expense file not found.")
        return

    # Get unique categories
    categories = sorted(set(row["category"] for row in rows))
    print("\n=== Existing Categories ===")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    # Choose category to inspect
    choice = input("Enter the number of the category to review/rename: ")
    try:
        index = int(choice) - 1
        old_cat = categories[index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    # Show all transactions in that category
    print(f"\n--- Transactions in '{old_cat}' ---")
    count = 0
    for row in rows:
        if row["category"] == old_cat:
            print(f"{row['id']}: ₹{row['amount']} | {row['description']} ({row['date']})")
            count += 1

    if count == 0:
        print("No transactions found.")
        return

    # Confirm rename
    confirm = input(f"\nDo you want to rename category '{old_cat}'? (y/n): ").lower()
    if confirm != 'y':
        print("Cancelled.")
        return

    new_cat = input(f"Enter new name for '{old_cat}': ").strip()
    if not new_cat:
        print("Empty name not allowed.")
        return

    # Apply changes
    for row in rows:
        if row["category"] == old_cat:
            row["category"] = new_cat

    # Save updated file
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ["id", "amount", "category", "description", "date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Category '{old_cat}' renamed to '{new_cat}' in {count} transaction(s).")

def main():
    initialize_csv()

while True:
    print("\n==== Expense Tracker ====")
    print("1. Add Expense")
    print("2. Import from Bank CSV")
    print("3. View Totals by Category")
    print("4. Edit Categories")  # 👈 new
    print("5. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        path = input("Enter full path to your bank CSV file: ").strip('"')
        import_bank_csv(path)
    elif choice == "3":
        view_totals_by_category()
    elif choice == "4":
        edit_category()
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
