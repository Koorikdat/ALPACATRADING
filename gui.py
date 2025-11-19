# Might build a gui to utilize the other modules and have a central dashboard for interactions.


import tkinter as tk
from tkinter import messagebox
import yfinance as yf

# Function to fetch ticker value
def load_ticker_value():
    ticker_symbol = ticker_entry.get().strip().upper()
    if not ticker_symbol:
        messagebox.showerror("Input Error", "Please enter a ticker symbol.")
        return

    try:
        ticker = yf.Ticker(ticker_symbol)
        price = ticker.history(period="1d")['Close'].iloc[-1]
        result_label.config(text=f"Current price of {ticker_symbol}: ${price:.2f}")
    except Exception as e:
        result_label.config(text=f"Error retrieving data for {ticker_symbol}.")

# GUI Setup
root = tk.Tk()
root.title("hi i am maisam")
root.geometry("500x500")

# Label + Entry
tk.Label(root, text="Enter Ticker Symbol:").pack(pady=10)
ticker_entry = tk.Entry(root, width=30)
ticker_entry.pack()

# Load Button
load_button = tk.Button(root, text="Load", command=load_ticker_value)
load_button.pack(pady=10)

# Result Display
result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

root.mainloop()
