import tkinter as tk
from tkinter import messagebox , ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ExpenseTrackerApp:
 def __init__(self, root):
        self.root = root
        self.root.title(" Pennywise Expense Tracker")
        self.root.geometry("600x1000")
        self.root.configure(bg="#2b2b2b")  
        
        self.expenses_categories = []
        self.expenses_values = []
       
        
        self.title_label= tk.Label(root,text="Budget Tracker Application", font=("Verdana", 12))
        self.title_label.pack(pady=20)
        
        self.category_frame = tk.Frame(root)
        self.category_frame.pack(pady=10)
        self.category_label = tk.Label(self.category_frame, text="Expense Category:")
        self.category_label.pack(side=tk.LEFT, padx=5)
       

        self.category_scrollbar = ttk.Scrollbar(self.category_frame, orient="vertical")
        self.category_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.expense_options = ["Food", "Transportation", "Housing", "Entertainment", "Utilities", "Education", "Healthcare", "Other"]

        self.selected_category = tk.StringVar()
        self.selected_category.set(self.expense_options[0]) 
        self.category_option = tk.OptionMenu(self.category_frame, self.selected_category, *self.expense_options)
        self.selected_category.trace("w", self.update_category_entry)
        
        self.category_option = tk.OptionMenu(self.category_frame, self.selected_category, *self.expense_options)
        self.category_option.config(width=40)
        self.category_option.pack(side=tk.LEFT, padx=5)

        self.custom_category_var = tk.StringVar()
        self.custom_category_entry = tk.Entry(self.category_frame, width=40)
        self.custom_category_entry.pack(side=tk.LEFT, padx=5)
        self.custom_category_entry.pack_forget() 
       
        self.value_frame = tk.Frame(root)
        self.value_frame.pack(pady=20)
        self.value_label = tk.Label(self.value_frame, text="Expense Value:")
        self.value_label.pack(side=tk.LEFT, padx=5)
        self.value_entry = tk.Entry(self.value_frame, width=40)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=20)
        self.add_button = tk.Button(self.buttons_frame, text="Add Expense", command=self.add_expense, width=15, bg="lightgreen")
        self.add_button.pack(side=tk.LEFT, padx=10)
        self.plot_button = tk.Button(self.buttons_frame, text="Plot Pie Chart", command=self.plot_chart, width=15, bg="lightblue")
        self.plot_button.pack(side=tk.LEFT, padx=10)
        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_data, width=15, bg="lightcoral")
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.listbox_frame = tk.Frame(root)
        self.listbox_frame.pack(pady=20)
        self.expenses_listbox = tk.Listbox(self.listbox_frame, width=50, height=10)
        self.expenses_listbox.pack(side=tk.LEFT, padx=10, pady=10)
        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient="vertical")
        self.scrollbar.config(command=self.expenses_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.expenses_listbox.config(yscrollcommand=self.scrollbar.set)

        self.chart_frame =tk.Frame(root)
        self.chart_frame.pack(pady=20)

 def update_category_entry(self, *args):
        selected_category = self.selected_category.get()
        if selected_category == "Other":
            self.custom_category_entry.pack(side=tk.LEFT, padx=5) 
        else:
            self.custom_category_entry.pack_forget()       
           
 def add_expense(self):
    category = self.selected_category.get()  
    if category == "Other":
        category = self.custom_category_entry.get()
        if not category:
            messagebox.showwarning("Input Error", "Please enter a custom category.")
            return
        else:
             self.custom_category_entry.pack_forget() 
    value = self.value_entry.get()
    
    if not category or not value:
        messagebox.showwarning("Input Error", "Please enter both category and value.")
        return

    try:
        value = float(value)
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid number for the value.")
        return

    self.expenses_categories.append(category)
    self.expenses_values.append(value)
    self.expenses_listbox.insert(tk.END, f"{category}: ${value:.2f}")

    self.value_entry.delete(0, tk.END)
    if self.custom_category_entry.winfo_ismapped():
        self.custom_category_entry.delete(0, tk.END)


 def plot_chart(self):
     if not self.expenses_categories or not self.expenses_values:
        messagebox.showwarning("Data Error", "No expenses to plot.")
        return

     fig = Figure(figsize=(6, 4))  
     ax = fig.add_subplot(111)
     colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6', '#c4e17f', '#76d7c4', '#f7b7a3', '#ffccff']
     wedges, texts, autotexts = ax.pie(self.expenses_values, labels=self.expenses_categories, colors=colors[:len(self.expenses_categories)], autopct='%1.1f%%', startangle=140)
        
     ax.set_title('Expense Distribution')
    
     for i, a in enumerate(autotexts):
        a.set_text(f'{self.expenses_values[i]:.2f}\n({a.get_text()})')
    
     plt.legend(wedges, self.expenses_categories, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
     for widget in self.chart_frame.winfo_children():
            widget.destroy()

     canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
     canvas.draw()
     canvas.get_tk_widget().pack()


 def reset_data(self):
         self.expenses_categories = []
         self.expenses_values = []
         self.expenses_listbox.delete(0, tk.END)
         for widget in self.chart_frame.winfo_children():  
            widget.destroy()
         messagebox.showinfo("Reset", "All data has been reset.")

def update_category_entry(self, event=None):
    selected_category = self.selected_category.get()
    if selected_category == "Other":
        self.custom_category_entry.pack(side=tk.LEFT, padx=5)
    else:
        self.custom_category_entry.pack_forget()


root = tk.Tk() 
a= ExpenseTrackerApp(root)  
root.mainloop ()  


