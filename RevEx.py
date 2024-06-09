import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json

class Expense:
    def __init__(self, date, amount, category, description):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

    def __repr__(self):
        return f"Expense(date={self.date}, amount={self.amount}, category={self.category}, description='{self.description}')"

    def to_dict(self):
        return {
            'date': self.date.strftime("%Y-%m-%d"),
            'amount': self.amount,
            'category': self.category,
            'description': self.description
        }

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, date, amount, category, description):
        expense = Expense(date, amount, category, description)
        self.expenses.append(expense)

    def list_expenses(self):
        return self.expenses

    def get_expenses_by_category(self, category):
        return [expense for expense in self.expenses if expense.category == category]

    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expenses)

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
        else:
            raise IndexError("Expense index out of range")

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump([expense.to_dict() for expense in self.expenses], file)

    def load_from_file(self, filename):
        self.expenses = []
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for item in data:
                    date = datetime.strptime(item['date'], "%Y-%m-%d").date()
                    self.add_expense(date, float(item['amount']), item['category'], item['description'])
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading from file: {e}")

class ExpenseTrackerApp:
    def __init__(self, root):
        self.tracker = ExpenseTracker()
        self.tracker.load_from_file('expenses.json')

        self.root = root
        self.root.title("Expense Tracker")

        self.root.geometry("600x1000")

        self.create_widgets()

    def create_widgets(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        self.form_frame = tk.Frame(self.root)
        self.form_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.form_frame.grid_columnconfigure(0, weight=1)
        self.form_frame.grid_columnconfigure(1, weight=1)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.button_frame.grid_columnconfigure(0, weight=1)

        self.date_label = tk.Label(self.form_frame, text="Date (YYYY-MM-DD):", font=("Verdana", 12))
        self.date_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.date_entry = tk.Entry(self.form_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.amount_label = tk.Label(self.form_frame, text="Amount:", font=("Verdana", 12))
        self.amount_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.amount_entry = tk.Entry(self.form_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.category_label = tk.Label(self.form_frame, text="Category:", font=("Verdana", 12))
        self.category_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.category_entry = tk.Entry(self.form_frame)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.description_label = tk.Label(self.form_frame, text="Description:", font=("Verdana", 12))
        self.description_label.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.description_entry = tk.Entry(self.form_frame)
        self.description_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.add_button = tk.Button(self.button_frame, text="Add Expense", command=self.add_expense, font=("Verdana", 12))
        self.add_button.grid(row=0, column=0, pady=5, sticky='n')

        self.view_all_button = tk.Button(self.button_frame, text="View All Expenses", command=self.view_expenses, font=("Verdana", 12))
        self.view_all_button.grid(row=1, column=0, pady=5, sticky='n')

        self.view_by_category_button = tk.Button(self.button_frame, text="View by Category", command=self.view_expenses_by_category, font=("Verdana", 12))
        self.view_by_category_button.grid(row=2, column=0, pady=5, sticky='n')

        self.view_total_button = tk.Button(self.button_frame, text="View Total Expenses", command=self.view_total_expenses, font=("Verdana", 12))
        self.view_total_button.grid(row=3, column=0, pady=5, sticky='n')

        self.delete_button = tk.Button(self.button_frame, text="Delete Selected Expense", command=self.delete_expense, font=("Verdana", 12))
        self.delete_button.grid(row=4, column=0, pady=5, sticky='n')

        self.history_button = tk.Button(self.button_frame, text="Spending History", command=self.show_history, font=("Verdana", 12))
        self.history_button.grid(row=5, column=0, pady=5, sticky='n')


        self.tree = ttk.Treeview(self.root, columns=("date", "amount", "category", "description"), show='headings')
        self.tree.heading("date", text="Date")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def add_expense(self):
        try:
            date_str = self.date_entry.get()
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive")
            category = self.category_entry.get()
            description = self.description_entry.get()
            self.tracker.add_expense(date, amount, category, description)
            self.update_treeview()
            self.update_total_expenses()
            messagebox.showinfo("Success", "Expense added!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, expense in enumerate(self.tracker.list_expenses()):
            self.tree.insert("", "end", iid=idx, values=(expense.date, expense.amount, expense.category, expense.description))

    def view_expenses(self):
        self.update_treeview()
        messagebox.showinfo("Info", "All expenses displayed in the table.")

    def view_expenses_by_category(self):
        category = self.category_entry.get()
        expenses = self.tracker.get_expenses_by_category(category)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, expense in enumerate(expenses):
            self.tree.insert("", "end", iid=idx, values=(expense.date, expense.amount, expense.category, expense.description))
        messagebox.showinfo(f"Expenses in {category}", f"Expenses in category '{category}' are displayed in the table.")

    def view_total_expenses(self):
        total = self.tracker.get_total_expenses()
        messagebox.showinfo("Total Expenses", f"Total Expenses: ${total}")

    def update_total_expenses(self):
        total = self.tracker.get_total_expenses()
        self.total_expenses_label.config(text=f"Total Expenses: ${total}")

    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No expense selected to delete")
            return

        try:
            index = int(selected_item[0])
            self.tracker.delete_expense(index)
            self.update_treeview()
            self.update_total_expenses()
            messagebox.showinfo("Success", "Expense deleted!")
        except IndexError as e:
            messagebox.showerror("Error", f"Error deleting expense: {e}")

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Spending History")

        history_tree = ttk.Treeview(history_window, columns=("date", "amount", "category", "description"), show='headings')
        history_tree.heading("date", text="Date")
        history_tree.heading("amount", text="Amount")
        history_tree.heading("category", text="Category")
        history_tree.heading("description", text="Description")
        history_tree.pack(fill=tk.BOTH, expand=True)

        for idx, expense in enumerate(self.tracker.list_expenses()):
            history_tree.insert("", "end", iid=idx, values=(expense.date, expense.amount, expense.category, expense.description))



    def on_closing(self):
        self.tracker.save_to_file('expenses.json')
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()