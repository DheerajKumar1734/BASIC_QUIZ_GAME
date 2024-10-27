import json
from datetime import datetime

# File to store expenses
FILE_PATH = 'expenses.json'

# Load existing data or initialize an empty list
def load_expenses():
    try:
        with open(FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(FILE_PATH, 'w') as file:
        json.dump(expenses, file, indent=4)

# Add a new expense entry
def add_expense(expenses):
    try:
        amount = float(input("Enter the amount spent: "))
        description = input("Enter a brief description: ")
        category = input("Enter the category (e.g., food, transportation, entertainment): ")
        date = datetime.now().strftime('%Y-%m-%d')

        expenses.append({
            'date': date,
            'amount': amount,
            'description': description,
            'category': category
        })
        save_expenses(expenses)
        print("Expense added successfully.")
    except ValueError:
        print("Invalid input. Please enter a valid number for the amount.")

# Display expenses by category or month
def display_summary(expenses):
    option = input("View summary by (1) month or (2) category? ")
    
    if option == '1':
        month = input("Enter the month (YYYY-MM): ")
        monthly_total = 0
        for expense in expenses:
            if expense['date'].startswith(month):
                print(f"{expense['date']} - {expense['category']} - ${expense['amount']}: {expense['description']}")
                monthly_total += expense['amount']
        print(f"Total for {month}: ${monthly_total}")
    
    elif option == '2':
        category = input("Enter the category: ")
        category_total = 0
        for expense in expenses:
            if expense['category'].lower() == category.lower():
                print(f"{expense['date']} - ${expense['amount']}: {expense['description']}")
                category_total += expense['amount']
        print(f"Total for {category}: ${category_total}")
    
    else:
        print("Invalid option selected.")

# Main function 
def main():
    expenses = load_expenses()
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            display_summary(expenses)
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()