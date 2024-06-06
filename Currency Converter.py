from currency_converter import CurrencyConverter
import tkinter as tk

c = CurrencyConverter()

def clicked():
    amount = float(entry1.get())  # Changed to float to handle decimals
    cur1 = entry2.get()
    cur2 = entry3.get()
    data = c.convert(amount, cur1, cur2)
    label4.config(text=data)  # Update text of existing label

window = tk.Tk()
window.geometry("500x360")
window.title("Pennywise Converter")

label = tk.Label(window, text="Currency Converter", font="Times 20 bold")
label.place(x=120, y=40)

label1 = tk.Label(window, text="Enter amount here:", font="Times 16 bold")
label1.place(x=70, y=100)
entry1 = tk.Entry(window)

label2 = tk.Label(window, text="Enter your currency here:", font="Times 16 bold")
label2.place(x=30, y=150)
entry2 = tk.Entry(window)

label3 = tk.Label(window, text="Enter your desired currency:", font="Times 16 bold")
label3.place(x=15, y=200)
entry3 = tk.Entry(window)

button = tk.Button(window, text="click", font="Times 16 bold", command=clicked)
button.place(x=220, y=250)

entry1.place(x=270, y=105)
entry2.place(x=270, y=155)
entry3.place(x=270, y=205)

# Create label for displaying result
label4 = tk.Label(window, text="", font="Times 16 bold")
label4.place(x=200, y=300)

window.mainloop()

                