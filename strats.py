# strategies.py
from utils import get_bars, get_current_price, buy_stock
import json
import ssl
from urllib.request import urlopen, Request
import sqlite3
import pandas as pd

def simple_algo(ticker="AAPL", threshold=200):
    bars = get_bars(ticker, "1Min", 5)
    current_price = bars['close'].iloc[-1]

    print(f"{ticker} is currently at ${current_price:.2f}")

    if current_price < threshold:
        print(f"{ticker} is under ${threshold}, buying 1 share.")
        buy_stock(ticker, 1)
    else:
        print(f"{ticker} is above ${threshold}, not buying.")
