import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from main import Transaction, insert_transaction, edit_expense, delete_transaction_by_item, Budget, categories

class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("Expense Tracker")

        label_options = {'font': ('Arial', 14)}  # Define font options for labels
        entry_options = {'font': ('Arial', 14)}  # Define font options for entry fields

        self.label = tk.Label(master, text="Expense Tracker Menu", font=("Courier", 44))
        self.label.pack(pady=50)

        style = ttk.Style()
        style.theme_create('custom_theme', parent='alt', settings={
            "TButton": {
                "configure": {
                    "background": "#3366FF",
                    "font": ('Helvetica', 14),
                    "foreground": "white",
                    "borderwidth": 2,
                    "relief": "raised",
                    "padding": 10,
                    "bordercolor": "#3366FF",
                    "borderradius": 10,
                },
                "map": {
                    "background": [("active", "#003366"), ("disabled", "#CCCCCC")],
                }
            }
        })
        style.theme_use('custom_theme')

        self.add_button = ttk.Button(master, text="Add Expense", command=self.display_add_expense_window, style='Custom.TButton')
        self.add_button.pack(pady=10)

        self.edit_button = ttk.Button(master, text="Edit Expense", command=self.display_edit_expense_window, style='Custom.TButton')
        self.edit_button.pack(pady=10)

        self.delete_button = ttk.Button(master, text="Delete Expense", command=self.delete_expense, style='Custom.TButton')
        self.delete_button.pack(pady=10)

        self.view_button = ttk.Button(master, text="View Expenses", command=self.view_expenses, style='Custom.TButton')
        self.view_button.pack(pady=10)

        self.set_budget_button = ttk.Button(master, text="Set Budget", command=self.set_budget, style='Custom.TButton')
        self.set_budget_button.pack(pady=10)

        self.track_spending_button = ttk.Button(master, text="Track Spending", command=self.track_spending, style='Custom.TButton')
        self.track_spending_button.pack(pady=10)

        self.exit_button = ttk.Button(master, text="Exit", command=master.quit, style='Custom.TButton')
        self.exit_button.pack(pady=10)

        self.root = None
        self.budgets = []

    def display_add_expense_window(self):
        self.add_expense_window = tk.Toplevel(self.master)
        self.add_expense_window.title("Add Expense")

        label_options = {'font': ('Arial', 14)}  # Define font options for labels
        entry_options = {'font': ('Arial', 14)}  # Define font options for entry fields

        self.date_label = tk.Label(self.add_expense_window, text="Enter transaction date (YYYY-MM-DD):", **label_options)
        self.date_label.pack()
        self.date_entry = tk.Entry(self.add_expense_window, **entry_options)
        self.date_entry.pack()

        self.amount_label = tk.Label(self.add_expense_window, text="Enter amount:", **label_options)
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.add_expense_window, **entry_options)
        self.amount_entry.pack()

        self.vendor_label = tk.Label(self.add_expense_window, text="Enter vendor:", **label_options)
        self.vendor_label.pack()
        self.vendor_entry = tk.Entry(self.add_expense_window, **entry_options)
        self.vendor_entry.pack()

        self.category_label = tk.Label(self.add_expense_window, text="Select expense category:", **label_options)
        self.category_label.pack()
        self.category_var = tk.StringVar(self.add_expense_window)
        self.category_dropdown = tk.OptionMenu(self.add_expense_window, self.category_var, *list(category.name for category in categories))
        self.category_dropdown.pack()

        self.subcategory_label = tk.Label(self.add_expense_window, text="Select expense subcategory:", **label_options)
        self.subcategory_label.pack()
        self.subcategory_var = tk.StringVar(self.add_expense_window)
        self.subcategory_dropdown = tk.OptionMenu(self.add_expense_window, self.subcategory_var, "")
        self.subcategory_dropdown.pack()

        self.item_label = tk.Label(self.add_expense_window, text="Enter item:", **label_options)
        self.item_label.pack()
        self.item_entry = tk.Entry(self.add_expense_window, **entry_options)
        self.item_entry.pack(pady=10)

        self.confirm_button = ttk.Button(self.add_expense_window, text="Confirm", command=self.add_expense, style='Custom.TButton')
        self.confirm_button.pack(pady=10)

        self.confirmation_label = tk.Label(self.add_expense_window, text="")
        self.confirmation_label.pack()

        self.category_var.trace_add("write", self.update_subcategory_options)

    def update_subcategory_options(self, *args):
        selected_category = self.category_var.get()
        for category in categories:
            if category.name == selected_category:
                self.subcategory_dropdown['menu'].delete(0, 'end')
                for keyword in category.keywords:
                    self.subcategory_dropdown['menu'].add_command(label=keyword, command=tk._setit(self.subcategory_var, keyword))

    def add_expense(self):
        date = self.date_entry.get()
        amount = float(self.amount_entry.get())
        vendor = self.vendor_entry.get()
        category = self.category_var.get()
        subcategory = self.subcategory_var.get()
        item = self.item_entry.get()

        new_transaction = Transaction(date, amount, vendor, subcategory, category, item)
        self.root = insert_transaction(self.root, new_transaction)
        self.confirmation_label.config(text="Expense added successfully!")

        self.add_expense_window.destroy()

    def display_edit_expense_window(self):
        self.edit_expense_window = tk.Toplevel(self.master)
        self.edit_expense_window.title("Edit Expense")

        label_options = {'font': ('Arial', 14)}  # Define font options for labels
        entry_options = {'font': ('Arial', 14)}  # Define font options for entry fields

        self.item_label = tk.Label(self.edit_expense_window, text="Enter the item of the expense to edit:", **label_options)
        self.item_label.pack()
        self.item_entry = tk.Entry(self.edit_expense_window, **entry_options)
        self.item_entry.pack()

        self.edit_confirm_button = ttk.Button(self.edit_expense_window, text="Edit", command=self.edit_expense, style='Custom.TButton')
        self.edit_confirm_button.pack()

        self.edit_confirmation_label = tk.Label(self.edit_expense_window, text="")
        self.edit_confirmation_label.pack()

    def edit_expense(self):
        item = self.item_entry.get()
        label_options = {'font': ('Arial', 14)}  # Define font options for labels
        entry_options = {'font': ('Arial', 14)}  # Define font options for entry fields
        current = self.root
        while current is not None:
            if item == current.transaction.item:
                break
            if item < current.transaction.item:
                current = current.left
            else:
                current = current.right

        if current is not None:
            self.edit_expense_window.destroy()
            self.edit_expense_window = tk.Toplevel(self.master)
            self.edit_expense_window.title("Edit Expense")

            self.amount_label = tk.Label(self.edit_expense_window, text="Amount:", **label_options)
            self.amount_label.pack()
            self.amount_entry = tk.Entry(self.edit_expense_window, **entry_options)
            self.amount_entry.insert(0, str(current.transaction.amount))
            self.amount_entry.pack()

            self.vendor_label = tk.Label(self.edit_expense_window, text="Vendor:", **label_options)
            self.vendor_label.pack()
            self.vendor_entry = tk.Entry(self.edit_expense_window, **entry_options)
            self.vendor_entry.insert(0, current.transaction.vendor)
            self.vendor_entry.pack()

            self.item_label = tk.Label(self.edit_expense_window, text="Item:", **label_options)
            self.item_label.pack()
            self.item_entry_edit = tk.Entry(self.edit_expense_window, **entry_options)
            self.item_entry_edit.insert(0, current.transaction.item)
            self.item_entry_edit.pack()

            self.confirm_edit_button = ttk.Button(self.edit_expense_window, text="Confirm", command=lambda: self.confirm_edit(current), style='Custom.TButton')
            self.confirm_edit_button.pack()

            self.edit_confirmation_label = tk.Label(self.edit_expense_window, text="")
            self.edit_confirmation_label.pack()

        else:
            self.edit_confirmation_label.config(text=f"Expense with item {item} not found.")

    def confirm_edit(self, current):
        amount = float(self.amount_entry.get())
        vendor = self.vendor_entry.get()
        item = self.item_entry_edit.get()

        current.transaction.amount = amount
        current.transaction.vendor = vendor
        current.transaction.item = item

        self.edit_confirmation_label.config(text="Expense updated successfully!")

    def delete_expense(self):
        item = simpledialog.askstring("Input", "Enter the item of the expense to delete:")
        if item is None:
            return
        self.root = delete_transaction_by_item(self.root, item)

    def view_expenses(self):
        if self.root is None:
            self.view_expenses_window = tk.Toplevel(self.master)
            self.view_expenses_window.title("View Expenses")

            empty_label = tk.Label(self.view_expenses_window, text="No expenses to display.")
            empty_label.pack()
        else:
            self.view_expenses_window = tk.Toplevel(self.master)
            self.view_expenses_window.title("View Expenses")

            scrollbar = tk.Scrollbar(self.view_expenses_window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            listbox = tk.Listbox(self.view_expenses_window, yscrollcommand=scrollbar.set)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.display_transactions(self.root, listbox)

            scrollbar.config(command=listbox.yview)

    def display_transactions(self, root, listbox):
        if root is not None:
            self.display_transactions(root.left, listbox)
            transaction_str = f"Date: {root.transaction.date}, Amount: {root.transaction.amount:.2f}, Vendor: {root.transaction.vendor}, Description: {root.transaction.description}, Category: {root.transaction.category}, Item: {root.transaction.item}"
            listbox.insert(tk.END, transaction_str)
            self.display_transactions(root.right, listbox)

    def set_budget(self):
        category = simpledialog.askstring("Input", "Enter category name:")
        if category is None:
            return
        amount = float(simpledialog.askstring("Input", f"Enter budget amount for {category}:"))
        
        for budget in self.budgets:
            if budget.category == category:
                budget.amount = amount
                break
        else:
            self.budgets.append(Budget(category, amount))

    def track_spending(self):
        if not self.budgets:
            self.track_spending_window = tk.Toplevel(self.master)
            self.track_spending_window.title("Track Spending")

            message_label = tk.Label(self.track_spending_window, text="Set budgets before tracking spending.")
            message_label.pack()
        else:
            self.track_spending_window = tk.Toplevel(self.master)
            self.track_spending_window.title("Track Spending")

            scrollbar = tk.Scrollbar(self.track_spending_window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            listbox = tk.Listbox(self.track_spending_window, yscrollcommand=scrollbar.set)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.display_spending(listbox)

            scrollbar.config(command=listbox.yview)

    def display_spending(self, listbox):
        total_spending = [0] * len(self.budgets)
        self.calculate_spending(self.root, total_spending)
        listbox.insert(tk.END, "Category \t Budget \t \t Spending \t Status")
        for budget, spending in zip(self.budgets, total_spending):
            status = 'Under Budget' if spending <= budget.amount else 'Over Budget'
            spending_str = f"{budget.category} \t     \t {budget.amount:.2f} \t     \t{spending:.2f} \t       \t{status}"
            listbox.insert(tk.END, spending_str)

    def calculate_spending(self, root, total_spending):
        if root is not None:
            for i, category in enumerate(categories):
                if root.transaction.category == category.name:
                    total_spending[i] += root.transaction.amount
                    break
            self.calculate_spending(root.left, total_spending)
            self.calculate_spending(root.right, total_spending)


root = tk.Tk()
app = ExpenseTrackerApp(root)
root.mainloop()
