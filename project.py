import sqlite3
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

top = Tk()
top.title("Expense Manager")
top['background'] = "#E0FFFF"
top.geometry("1000x600")

expense_connection = sqlite3.connect('expense.db')
wishlist_connection = sqlite3.connect('wlist.db')
daily_amt_connection = sqlite3.connect('daily_amt.db')
monthly_connection = sqlite3.connect('monthly.db')

expense_cursor = expense_connection.cursor()
wishlist_cursor = wishlist_connection.cursor()
daily_amt_cursor = daily_amt_connection.cursor()
monthly_cursor = monthly_connection.cursor()

# Create the 'expenses' table if it doesn't exist
expense_cursor.execute('''CREATE TABLE IF NOT EXISTS
               expenses(
                   id INTEGER PRIMARY KEY,
                   category TEXT,
                   amount REAL,
                   date DATE DEFAULT (datetime('now', 'localtime')),
                   hour INTEGER)''')
expense_connection.commit()

wishlist_cursor.execute('''CREATE TABLE IF NOT EXISTS
                wlist(
                    wishlist TEXT,
                    money REAL)''')
wishlist_connection.commit()

daily_amt_cursor.execute('''CREATE TABLE IF NOT EXISTS
                daily_amt(
                    total REAL,
                    call INTEGER)''')
daily_amt_connection.commit()

monthly_cursor.execute('''CREATE TABLE IF NOT EXISTS
                daily(
                    monthly_total REAL)''')
monthly_connection.commit()

t = 0.0

expense_categories = {
    '1': 'Food',
    '2': 'Transport',
    '3': 'Entertainment',
    '4': 'Taxes/Utilities',
    '5': 'Clothing',
    '6': 'Other'
}


def add_expense_gui():
    expense_window = Toplevel(top)
    expense_window['background'] = "#E0FFFF"
    expense_window.title("Add Expense")
    expense_window.geometry("500x500")

    amount_var = DoubleVar()
    selected_category_var = StringVar()
    selected_category_var.set('Food')  # Set a default category

    def submit_expense():
        category = selected_category_var.get()
        amount = amount_var.get()
        global t
        t += amount
        time = datetime.now()
        hr = time.hour
        minute = time.minute
        expense_cursor.execute("INSERT INTO expenses (category, amount, hour) VALUES (?, ?, ?)", (category, amount, hr))
        expense_connection.commit()
        expenses_label.config(text="Expense added successfully.", font=("Constantia", 13), )
        expense_window.destroy()

    Label(expense_window, text="Select Expense Category:", font=("Constantia", 14),bg="#8DB6CD").pack(pady=20)
    category_menu = OptionMenu(expense_window, selected_category_var, *expense_categories.values())
    category_menu.pack()

    Label(expense_window, text="Expense Amount:", font=("Constantia", 14),bg="#8DB6CD").pack(pady=35)
    Entry(expense_window, textvariable=amount_var).pack()

    Button(expense_window, text="Submit", font=("Constantia", 12), command=submit_expense, width=20,bg="#8DB6CD").pack()


def display_expenses_gui():
    expenses_window = Toplevel(top)
    expenses_window['background'] = "#E0FFFF"
    expenses_window.title("Expenses")
    expenses_window_piechartt = Toplevel(top)
    expenses_window_piechartt.title("piechart")

    scrollbar = Scrollbar(expenses_window)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(expenses_window, yscrollcommand=scrollbar.set, width=40)
    listbox.pack(expand=YES, fill=BOTH)

    expenses = {}
    expense_cursor.execute("SELECT category, amount FROM expenses")
    rows = expense_cursor.fetchall()

    for category, amount in rows:
        if category in expenses:
            expenses[category].append(amount)
        else:
            expenses[category] = [amount]

    for category, amount in expenses.items():
        expenses_text = f"Category: {category}, Amount: {amount}"
        listbox.insert(END, expenses_text)

    scrollbar.config(command=listbox.yview)

    # Display Monthly Expenses Bar Chart
    # expense_cursor.execute("SELECT strftime('%Y-%m', date) as month, SUM(amount) FROM expenses GROUP BY month")
    # expense_cursor.execute("SELECT strftime('%H:%M', hour) AS minute, SUM(amount) FROM expenses GROUP BY minute")
    expense_cursor.execute("SELECT SUM(amount), strftime('%H',date) FROM expenses GROUP BY strftime('%H',date)")
    monthly_rows = expense_cursor.fetchall()
    months = [int(row[1]) for row in monthly_rows]
    expenses = [row[0] for row in monthly_rows]

    fig, ax = plt.subplots()
    ax.bar(months, expenses, width=0.8)
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Expenses')
    ax.set_title('Monthly Expenses')

    canvas = FigureCanvasTkAgg(fig, master=expenses_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Display Category-wise Expenses Pie Chart
    expense_cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    category_rows = expense_cursor.fetchall()
    categories = [row[0] for row in category_rows]
    category_expenses = [row[1] for row in category_rows]

    fig2, ax2 = plt.subplots()
    ax2.pie(category_expenses, labels=categories, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax2.set_title('Category-wise Expenses')

    canvas2 = FigureCanvasTkAgg(fig2, master=expenses_window_piechartt)
    canvas_widget2 = canvas2.get_tk_widget()
    canvas_widget2.pack()


def wishlist_gui():
    wishlist_window = Toplevel(top)
    wishlist_window['background'] = "#E0FFFF"
    wishlist_window.title("Wishlist")

    def wishlist1():
        wishlist_input_window = Toplevel(wishlist_window)
        wishlist_input_window['background'] = "#E0FFFF"
        wishlist_input_window.title("Add to Wishlist")

        item_var = StringVar()
        amount_var = DoubleVar()

        def add_to_wishlist():
            item = item_var.get()
            amount = amount_var.get()
            global t
            t += amount
            wishlist_cursor.execute("INSERT INTO wlist (wishlist, money) VALUES (?, ?)", (item, amount))
            wishlist_connection.commit()
            wishlist_label.config(text="   Item added", font=("Constantia", 13))
            wishlist_input_window.destroy()

        Label(wishlist_input_window, text="Enter Wishlist Item:", font=("Constantia", 14),bg="#8DB6CD").pack(pady=20)
        Entry(wishlist_input_window, textvariable=item_var, font=("Constantia", 14)).pack(pady=20)

        Label(wishlist_input_window, text="Enter Amount:", font=("Constantia", 14),bg="#8DB6CD").pack(pady=20)
        Entry(wishlist_input_window, textvariable=amount_var, font=("Constantia", 14)).pack(pady=20)

        Button(wishlist_input_window, text="Submit", command=add_to_wishlist, font=("Constantia", 13),bg="#8DB6CD").pack(pady=20)

    def display_wishlist():
        wishlist_window.withdraw()  # Hide the wishlist window
        wishlist_display_window = Toplevel(top)
        wishlist_display_window['background'] = "#E0FFFF"
        wishlist_display_window.title("Wishlist Display")

        wishlist_cursor.execute("SELECT wishlist, money FROM wlist")
        row = wishlist_cursor.fetchall()
        for wishlist, money in row:
            wishlist_text = f"   {wishlist} - {money}"
            Label(wishlist_display_window, text=wishlist_text,  font=("Constantia", 13), bg="#8DB6CD").pack()

    def recommendations(income):
        flag = 0
        expenditure = 0.0
        savings = 0.0
        expense_cursor.execute("SELECT amount FROM expenses")
        row = expense_cursor.fetchall()
        for amount in row:
            expenditure += amount[0]
        savings = income - expenditure

        wishlist_cursor.execute("SELECT wishlist, money FROM wlist")
        rows = wishlist_cursor.fetchall()
        recommendations_text = ""
        for wishlist, money in rows:
            if money < (savings + 1000):
                flag = 1
                recommendations_text += f"You have saved up for: {wishlist} - {money}\n"
            else:
                continue
        if flag == 0:
            recommendations_text = "No recommendations this week :("

        recommendations_label.config(text=recommendations_text)

    def delete_wishlist():
        delete_window = Toplevel(top)
        delete_window['background'] = "#E0FFFF"
        delete_window.title("Delete Item")

        delete_var = StringVar()

        def delete():
            key = delete_var.get()
            wishlist_cursor.execute("DELETE FROM wlist WHERE wishlist = ?", (key,))
            wishlist_connection.commit()
            #delete_label.config(text="   Item deleted", font=("Constantia", 13)).pack()
            delete_label.config(text="   Item deleted", font=("Constantia", 13))
            delete_window.destroy()

        Label(delete_window, text="Enter item to delete:", font=("Constantia", 14),bg="#8DB6CD").pack(pady=20)
        Entry(delete_window, textvariable=delete_var).pack()
        Button(delete_window, text="Delete", font=("Constantia", 14), command=delete,bg="#8DB6CD").pack(pady=20)

    Button(wishlist_window, text="Add item to wishlist", font=("Constantia", 12), command=wishlist1, width=20,bg="#8DB6CD").pack()
    Button(wishlist_window, text="Display wishlist", font=("Constantia", 14), command=display_wishlist, width=20,bg="#8DB6CD").pack(
        pady=20)
    Button(wishlist_window, text="Recommendations", font=("Constantia", 14), command=lambda: recommendations(income),
           width=20,bg="#8DB6CD").pack(pady=20)
    Button(wishlist_window, text="Delete item from wishlist", font=("Constantia", 14), command=delete_wishlist,
           width=20,bg="#8DB6CD").pack(pady=20)
    Button(wishlist_window, text="Exit wishlist", font=("Constantia", 14), command=wishlist_window.destroy,
           width=20,bg="#8DB6CD").pack(pady=20)


income_window = Toplevel()
income_window['background'] = "#E0FFFF"
income_window.title("Monthly Income")
income_window.geometry("1500x700")
income_var = DoubleVar()


def submit_income():
    global income
    income = income_var.get()
    income_window.destroy()
def add_total():
    total_window = Toplevel(top)
    total_window['background'] = "#E0FFFF"
    total_window.title("Total Expenses")
    Label(total_window, text=f"Your total expenses for today are: {t}",bg="#8DB6CD", font=("Constantia", 14)).pack()

Label(income_window, text="Please enter your monthly income before you proceed:", font=("Constantia", 14),bg="#8DB6CD").pack(pady=20)
Entry(income_window, textvariable=income_var, font=("Constantia", 16)).pack(pady=20)
Button(income_window, text="Submit", font=("Constantia", 10), command=submit_income, height=2, width=20,bg="#8DB6CD").pack()

expenses_label = Label(top, text="")
wishlist_label = Label(top, text="")
recommendations_label = Label(top, text="")
delete_label = Label(top, text="")

Button(top, text="Add Expense", font=("Constantia", 16), command=add_expense_gui, width=30, height=2,bg="#8DB6CD").pack(pady=10)
Button(top, text="Display Expenses", font=("Constantia", 16), command=display_expenses_gui, width=30, height=2,bg="#8DB6CD").pack(
    pady=10)
Button(top, text="Wishlist", font=("Constantia", 16), command=wishlist_gui, width=30, height=2,bg="#8DB6CD").pack(pady=10)
Button(top, text="Today's total expense",  font=("Constantia", 16), command=add_total, width=30, height=2, bg="#8DB6CD").pack(pady=10)
Button(top, text="Quit", font=("Constantia", 16), command=top.destroy, width=30, height=2,bg="#8DB6CD").pack(pady=10)

expenses_label.pack()
wishlist_label.pack()
recommendations_label.pack()
delete_label.pack()

top.mainloop()