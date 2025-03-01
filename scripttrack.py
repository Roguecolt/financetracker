import json
import os

# File to store transactions
DATA_FILE = "transactions.json"

# Load existing transactions from file
def load_transactions():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Save transactions to file
def save_transactions(transactions):
    with open(DATA_FILE, "w") as file:
        json.dump(transactions, file, indent=4)

# Add a new transaction
def add_transaction(amount, type, category, date):
    transactions = load_transactions()
    new_transaction = {
        "id": len(transactions) + 1,
        "amount": amount,
        "type": type,
        "category": category,
        "date": date
    }
    transactions.append(new_transaction)
    save_transactions(transactions)
    print("Transaction added successfully!")

# View all transactions
def view_transactions():
    transactions = load_transactions()
    if not transactions:
        print("No transactions found.")
        return
    print("\nTransactions:")
    for t in transactions:
        print(f"[{t['id']}] {t['date']} | {t['type'].capitalize()} | {t['category']} | ${t['amount']}")

# Calculate balance
def calculate_balance():
    transactions = load_transactions()
    income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    return income - expenses

# Delete a transaction
def delete_transaction(transaction_id):
    transactions = load_transactions()
    updated_transactions = [t for t in transactions if t["id"] != transaction_id]
    
    if len(updated_transactions) == len(transactions):
        print("Transaction not found.")
    else:
        save_transactions(updated_transactions)
        print("Transaction deleted successfully!")

# Main menu
def main():
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Show Balance")
        print("4. Delete Transaction")
        print("5. Exit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            amount = float(input("Enter amount: "))
            type = input("Enter type (income/expense): ").strip().lower()
            category = input("Enter category: ")
            date = input("Enter date (YYYY-MM-DD): ")
            add_transaction(amount, type, category, date)
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            print(f"Current Balance: ${calculate_balance()}")
        elif choice == "4":
            transaction_id = int(input("Enter transaction ID to delete: "))
            delete_transaction(transaction_id)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
