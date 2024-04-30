MAX_CATEGORIES = 11
MAX_KEYWORDS_PER_CATEGORY = 10
HASH_TABLE_SIZE = 50

class Transaction:
    def __init__(self, date, amount, vendor, description, category, item):
        self.date = date
        self.amount = amount
        self.vendor = vendor
        self.description = description
        self.category = category
        self.item = item

class TreeNode:
    def __init__(self, transaction):
        self.transaction = transaction
        self.left = None
        self.right = None

class Budget:
    def __init__(self, category, amount):
        self.category = category
        self.amount = amount

class Category:
    def __init__(self, name, keywords, num_keywords):
        self.name = name
        self.keywords = keywords
        self.num_keywords = num_keywords

categories = [
    Category("Food", ["grocery", "restaurant", "dining", "food"], 4),
    Category("Rent", ["rent", "housing", "apartment"], 3),
    Category("Clothes", ["clothes", "shoes", "jewelry"], 3),
    Category("Entertainment", ["entertainment", "movies", "music", "cinema", "music"], 5),
    Category("Travel", ["travel", "flight", "hotel", "rental"], 4),
    Category("Miscellaneous", ["miscellaneous", "gift", "purchases", "subscriptions"], 4),
    Category("Pet", ["pet", "dog", "cat"], 3),
    Category("Health", ["health", "medical", "insurance", "pharmacy", "drug", "prescription"], 6),
    Category("Education", ["education", "school", "college", "university"], 4),
    Category("Electronics", ["electronics", "computer", "laptop", "phone", "tablet"], 5),
    Category("Home", ["home", "furnishings", "kitchen", "bathroom", "bedroom", "bathroom", "laundry"], 6),
    # Add more categories and their keywords as needed
]

def create_node(transaction):
    return TreeNode(transaction)

def insert_transaction(root, transaction):
    if root is None:
        return create_node(transaction)
    if transaction.date < root.transaction.date:
        root.left = insert_transaction(root.left, transaction)
    else:
        root.right = insert_transaction(root.right, transaction)
    return root

def print_transactions(root):
    if root is not None:
        print_transactions(root.left)
        print(f"Date: {root.transaction.date}, Amount: {root.transaction.amount:.2f}, Vendor: {root.transaction.vendor}, Description: {root.transaction.description}, Category: {root.transaction.category}, Item: {root.transaction.item}")
        print_transactions(root.right)

def recommend_category(description):
    for category in categories:
        for keyword in category.keywords:
            if keyword in description:
                return category.name
    return "Other"

def add_expense(root):
    new_transaction = Transaction(
        input("Enter transaction date (YYYY-MM-DD): "),
        float(input("Enter amount: ")),
        input("Enter vendor: "),
        "",
        "",
        ""
    )
    print("Select expense category:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category.name}")
    category_choice = int(input("Enter category choice: "))
    if category_choice < 1 or category_choice > len(categories):
        print("Invalid category choice.")
        return root
    new_transaction.category = categories[category_choice - 1].name

    print("Select expense subcategory:")
    for i, keyword in enumerate(categories[category_choice - 1].keywords, start=1):
        print(f"{i}. {keyword}")
    subcategory_choice = int(input("Enter subcategory choice: "))
    if subcategory_choice < 1 or subcategory_choice > len(categories[category_choice - 1].keywords):
        print("Invalid subcategory choice.")
        return root
    new_transaction.description = categories[category_choice - 1].keywords[subcategory_choice - 1]

    new_transaction.item = input("Enter item: ")

    root = insert_transaction(root, new_transaction)
    print("Expense added successfully!")
    return root

def edit_expense(root):
    item = input("Enter the item of the expense to edit: ")
    current = root
    parent = None
    while current is not None:
        if item == current.transaction.item:
            break
        parent = current
        if item < current.transaction.item:
            current = current.left
        else:
            current = current.right
    if current is not None:
        print("Enter updated transaction details:")
        current.transaction.amount = float(input("Amount: "))
        current.transaction.vendor = input("Vendor: ")
        current.transaction.description = recommend_category(current.transaction.vendor)
        current.transaction.category = recommend_category(current.transaction.description)
        current.transaction.item = input("Item: ")
        print("Expense updated successfully!")
    else:
        print(f"Expense with item {item} not found.")
    return root

def delete_transaction_by_item(root, item):
    if root is None:
        return root
    if item < root.transaction.item:
        root.left = delete_transaction_by_item(root.left, item)
    elif item > root.transaction.item:
        root.right = delete_transaction_by_item(root.right, item)
    else:
        if root.left is None:
            temp = root.right
            del root
            return temp
        elif root.right is None:
            temp = root.left
            del root
            return temp
        temp = root.right
        while temp.left is not None:
            temp = temp.left
        root.transaction = temp.transaction
        root.right = delete_transaction_by_item(root.right, temp.transaction.item)
    return root

def delete_expense(root):
    item = input("Enter the item of the expense to delete: ")
    root = delete_transaction_by_item(root, item)
    print("Expense deleted successfully!")
    return root

# def set_budget(budgets):
#     num_budgets = int(input("Enter the number of budget categories: "))
#     for i in range(num_budgets):
#         category = input("Enter category name: ")
#         amount = float(input(f"Enter budget amount for {category}: "))
#         budgets.append(Budget(category, amount))


def set_budget(budgets):
    print("Select category to set budget for:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category.name}")
    category_choice = int(input("Enter category choice: "))
    if category_choice < 1 or category_choice > len(categories):
        print("Invalid category choice.")
        return budgets
    category_name = categories[category_choice - 1].name

    for budget in budgets:
        if budget.category == category_name:
            budget.amount = float(input(f"Enter budget amount for {category_name}: "))
            print("Budget updated successfully!")
            return budgets

    new_budget = Budget(category_name, float(input(f"Enter budget amount for {category_name}: ")))
    budgets.append(new_budget)
    print("Budget set successfully!")
    return budgets



def track_spending(root, budgets):
    total_spending = [0] * len(budgets)
    calculate_spending(root, total_spending)
    print("Category\tBudget\t\tSpending\tStatus")
    for budget, spending in zip(budgets, total_spending):
        print(f"{budget.category}\t\t{budget.amount:.2f}\t\t{spending:.2f}\t\t{'Under Budget' if spending <= budget.amount else 'Over Budget'}")



def calculate_spending(root, total_spending):
    if root is not None:
        for i, category in enumerate(categories):
            if root.transaction.category == category.name:
                total_spending[i] += root.transaction.amount
                break
        calculate_spending(root.left, total_spending)
        calculate_spending(root.right, total_spending)



def main():
    root = None
    budgets = []
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. Edit Expense")
        print("3. Delete Expense")
        print("4. View Expenses")
        print("5. Set Budget")
        print("6. Track Spending")
        print("7. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            root = add_expense(root)
        elif choice == 2:
            root = edit_expense(root)
        elif choice == 3:
            root = delete_expense(root)
        elif choice == 4:
            print("\nAll Transactions:")
            print_transactions(root)
        elif choice == 5:
            set_budget(budgets)
        elif choice == 6:
            if not budgets:
                print("Set budgets before tracking spending.")
            else:
                track_spending(root, budgets)
        elif choice == 7:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
