# utils.py - Building on your existing code
import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
import json
import ssl
from urllib.request import urlopen, Request
import sqlite3
import pandas as pd
import time
from datetime import datetime, timedelta
import logging

# Configure logging - need to set up logging for better debugging and tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.getenv('APCA_API_KEY_ID')
API_SECRET = os.getenv('APCA_API_SECRET_KEY')
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

#get_account_status()	            Returns "ACTIVE" if ready to trade
#get_positions()	                Prints and returns position data
#get_bars()                      	Returns OHLCV historical data
#buy_stock()	                    Places market buy order
#sell_stock()	                    Places market sell order safely
#get_current_price()	            Gets latest trade price
#get_account_balance()	            Prints and returns account metrics
#get_latest_bar():                  Returns the most recent OHLCV bar
#has_position()                     Returns True if you currently hold shares of the stock.
#get_order_history()                Retrieves historical order data with optional filters.
#place_limit_order()                Places a limit order for a specified stock, quantity, and price.
#place_stop_loss()                  Places a stop-loss order for a specified stock and quantity at a given stop price.
#get_watchlist_stocks()             Retrieves all watchlists and the stocks within them.
#create_watchlist()                 Creates a new watchlist with the specified name and symbols.
#get_portfolio_performance()        Calculates and returns portfolio performance metrics over a specified number of days.
#get_multiple_prices()              Retrieves the current prices for a list of symbols.
#calculate_position_metrics()       Calculates detailed metrics for a specific stock position, including unrealized P&L and percentages.
#get_market_calendar()              Retrieves the market calendar, showing open and close times for upcoming days.
#risk_assessment()                  Assesses the risk of a potential trade, calculating position size, suggested stop-loss, and maximum potential loss.
#database_logger()                  Initializes the SQLite database, creating tables for trade logs and daily performance.
#log_trade_to_db()                  Logs a completed trade to the SQLite database.
#get_trade_history_from_db()        Retrieves trade history from the local SQLite database for a specified number of past days.






#Should return something like "ACTIVE"
def get_account_status():
    account = api.get_account()
    return account.status

# For each position, you can access:
#   - symbol: the stock ticker (e.g., "AAPL")
#   - qty: number of shares owned
#   - avg_entry_price: the average price per share you paid
#   - market_value: current market value of the position
#   - unrealized_pl: current unrealized profit or loss
#   - side: 'long' or 'short'
#  print(f"Symbol: {position['symbol']}, Quantity: {position['qty']}, Side: {position['side']}")

# positions = get_positions()
# for pos in positions:
#     print(f"{pos['symbol']} → {pos['qty']} shares, P/L: ${pos['unrealized_pl']:.2f}")
def get_positions(show: bool = False):
    positions = api.list_positions()
    position_data = []

    for pos in positions:
        position_details = {
            "symbol": pos.symbol,
            "side": pos.side,
            "qty": float(pos.qty),
            "avg_entry_price": float(pos.avg_entry_price),
            "market_value": float(pos.market_value),
            "unrealized_pl": float(pos.unrealized_pl),
        }
        position_data.append(position_details)

        if show:
            print(f"Symbol: {position_details['symbol']}")
            print(f"  Side: {position_details['side']}")
            print(f"  Quantity: {position_details['qty']}")
            print(f"  Average Entry Price: ${position_details['avg_entry_price']:.2f}")
            print(f"  Market Value: ${position_details['market_value']:.2f}")
            print(f"  Unrealized P/L: ${position_details['unrealized_pl']:.2f}")
            print("-" * 25)

    return position_data

# get_bars() retrieves historical OHLCV bar data as a Pandas DataFrame.
# limit = minutes, show = print output
# Example usage:
#   bars = get_bars("MSFT", timeframe="1Day", limit=50)
#   latest_close = bars['close'].iloc[-1]


# Returned DataFrame columns:
#   open         - Price at the start of the bar
#   high         - Highest price during the bar
#   low          - Lowest price during the bar
#   close        - Price at the end of the bar
#   volume       - Number of shares traded
#   trade_count  - Number of trades (not always available)
#   vwap         - Volume-weighted average price
#   timestamp    - Datetime the bar represents (index, in UTC)
def get_bars(symbol, timeframe, limit=100, show=False):
    bars_df = api.get_bars(symbol, timeframe, limit=limit).df

    if show:
        print(f"--- Last 5 Bars for {symbol} ({timeframe}) ---")
        print(bars_df[['open', 'high', 'low', 'close', 'volume']].tail())
        print("-" * 40)

    return bars_df

# buy_stock(ticker, quantity)
def buy_stock(symbol="AAPL", qty=1):
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print(f"Submitted buy order for {qty} shares of {symbol}")
        return order
    except Exception as e:
        print(f"Error submitting buy order for {symbol}: {e}")
        return None

# get_current_price("AAPL")
def get_current_price(ticker: str) -> float:
    try:
        latest_trade = api.get_latest_trade(ticker)
        return latest_trade.price
    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
        return None


# sell_stock("AAPL", 2)
# sell_stock("AAPL", 2)
def sell_stock(symbol: str, qty: int = 1):
    """
    Attempts to sell the given quantity of a stock if owned.
    Verifies that you hold enough shares before selling.

    Args:
        symbol (str): Ticker symbol (e.g., "AAPL")
        qty (int): Number of shares to sell
    """
    try:
        position = api.get_position(symbol)
        owned_qty = int(float(position.qty))

        if qty <= owned_qty:
            api.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            print(f"Submitted sell order for {qty} shares of {symbol}")
            print(u'\u2500' * 10)
        else:
            print(f"Cannot sell {qty} shares of {symbol}. Only {owned_qty} owned.")
            print(u'\u2500' * 10)
    except Exception as e:
        print(f"Error fetching position for {symbol}: {e}")
        print(u'\u2500' * 10)

# balance = get_account_balance()
# print(f"Available Cash: ${balance['cash']}")
def get_account_balance():
    account = api.get_account()
    
    cash = float(account.cash)
    portfolio_value = float(account.portfolio_value)
    buying_power = float(account.buying_power)
    equity = float(account.equity)
    multiplier = account.multiplier
    long_market_value = float(account.long_market_value)
    short_market_value = float(account.short_market_value)

    print(f"Cash Available: ${cash:.2f}")
    print(f"Buying Power: ${buying_power:.2f}")
    print(f"Equity: ${equity:.2f}")
    print(f"Portfolio Value: ${portfolio_value:.2f}")
    print(f"Long Market Value: ${long_market_value:.2f}")
    print(f"Short Market Value: ${short_market_value:.2f}")
    print(f"Margin Multiplier: {multiplier}")
    
    return {
        "cash": cash,
        "buying_power": buying_power,
        "equity": equity,
        "portfolio_value": portfolio_value,
        "long_market_value": long_market_value,
        "short_market_value": short_market_value,
        "multiplier": multiplier
    }

# get_latest_bar(symbol, timeframe) returns the most recent OHLCV bar.
# Useful for quick access to the latest open, high, low, close, volume values.
#
# Example:
#   bar = get_latest_bar("AAPL", "1Min")
#   print(f"AAPL Latest Close: ${bar['close']:.2f}") if bar is not None else print("No bar data.")

def get_latest_bar(symbol="AAPL", timeframe="1Min"):
    bars = get_bars(symbol, timeframe, limit=1)
    return bars.iloc[-1] if not bars.empty else None

# has_position(symbol) returns True if you currently hold shares of the stock.
#
# Example:
#   if has_position("AAPL"):
#       print("You currently own AAPL.")
#   else:
#       print("You do not own AAPL.")
def has_position(symbol: str) -> bool:
    try:
        position = api.get_position(symbol)
        return float(position.qty) > 0
    except:
        return False

# get_order_history(symbol=None, status=None, limit=50) retrieves historical order data.
# You can filter by symbol and status (e.g., 'open', 'closed').
def get_order_history(symbol=None, status=None, limit=50):
    """Get order history with optional filtering"""
    try:
        orders = api.list_orders(
            status=status or 'all',
            limit=limit,
            nested=True
        )
        
        order_data = []
        for order in orders:
            if symbol and order.symbol != symbol:
                continue
                
            order_details = {
                "id": order.id,
                "symbol": order.symbol,
                "qty": float(order.qty),
                "side": order.side,
                "order_type": order.order_type,
                "time_in_force": order.time_in_force,
                "status": order.status,
                "created_at": order.created_at,
                "filled_qty": float(order.filled_qty or 0),
                "filled_avg_price": float(order.filled_avg_price or 0)
            }
            order_data.append(order_details)
        
        return order_data
    except Exception as e:
        print(f"Error fetching order history: {e}")
        return []

# place_limit_order(symbol, qty, price, side='buy', time_in_force='gtc')
# Places a limit order for the specified stock, quantity, and price.
def place_limit_order(symbol, qty, price, side='buy', time_in_force='gtc'):
    """Place a limit order"""
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='limit',
            time_in_force=time_in_force,
            limit_price=price
        )
        print(f"Submitted {side} limit order for {qty} shares of {symbol} at ${price}")
        return order
    except Exception as e:
        print(f"Error submitting limit order for {symbol}: {e}")
        return None

# place_stop_loss(symbol, qty, stop_price, side='sell')
# Places a stop-loss order for the specified stock and quantity at the given stop price.
#   place_stop_loss("AAPL", 1, 150.00)
def place_stop_loss(symbol, qty, stop_price, side='sell'):
    """Place a stop loss order"""
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='stop',
            time_in_force='gtc',
            stop_price=stop_price
        )
        print(f"Submitted stop loss order for {qty} shares of {symbol} at ${stop_price}")
        return order
    except Exception as e:
        print(f"Error submitting stop loss order for {symbol}: {e}")
        return None

# get_watchlist_stocks() retrieves all watchlists and their stocks.
def get_watchlist_stocks():
    """Get all watchlists and their stocks"""
    try:
        watchlists = api.list_watchlists()
        watchlist_data = []
        
        for watchlist in watchlists:
            stocks = []
            for asset in watchlist.assets:
                stocks.append(asset.symbol)
            
            watchlist_data.append({
                "id": watchlist.id,
                "name": watchlist.name,
                "stocks": stocks,
                "created_at": watchlist.created_at
            })
        
        return watchlist_data
    except Exception as e:
        print(f"Error fetching watchlists: {e}")
        return []

# create_watchlist(name, symbols) creates a new watchlist with the specified name and symbols.
#   create_watchlist("My Watchlist", ["AAPL", "GOOGL",
def create_watchlist(name, symbols):
    """Create a new watchlist with given symbols"""
    try:
        watchlist = api.create_watchlist(name, symbols)
        print(f"Created watchlist '{name}' with {len(symbols)} symbols")
        return watchlist
    except Exception as e:
        print(f"Error creating watchlist: {e}")
        return None

# get_portfolio_performance(days=30) calculates and returns portfolio performance metrics over a specified number of days.
#   Example usage:
#   performance = get_portfolio_performance(30)
#   print(f"Total return over last 30 days: {performance['total_return_pct
def get_portfolio_performance(days=30):
    """Calculate portfolio performance over specified days"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        portfolio_history = api.get_portfolio_history(
            timeframe='1D',
            start=start_date.isoformat(),
            end=end_date.isoformat()
        )
        
        if not portfolio_history.equity:
            return None
        
        start_value = portfolio_history.equity[0]
        end_value = portfolio_history.equity[-1]
        total_return = ((end_value - start_value) / start_value) * 100
        
        performance = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "start_value": start_value,
            "end_value": end_value,
            "total_return_pct": total_return,
            "total_return_dollar": end_value - start_value,
            "equity_history": portfolio_history.equity,
            "timestamps": portfolio_history.timestamp
        }
        
        return performance
    except Exception as e:
        print(f"Error calculating portfolio performance: {e}")
        return None

# get_multiple_prices(symbols) retrieves the current prices for a list of symbols.
#   Example usage:
#   prices = get_multiple_prices(["AAPL", "GOOGL", "MSFT
def get_multiple_prices(symbols):
    """Get current prices for multiple symbols at once"""
    prices = {}
    for symbol in symbols:
        try:
            price = get_current_price(symbol)
            prices[symbol] = price
        except:
            prices[symbol] = None
    return prices

# calculate_position_metrics(symbol) calculates detailed metrics for a specific stock position.
def database_logger():
    """Initialize SQLite database for trade logging"""
    conn = sqlite3.connect('trading_log.db')
    cursor = conn.cursor()
    
    # Create trades table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            symbol TEXT,
            side TEXT,
            quantity INTEGER,
            price REAL,
            total_value REAL,
            strategy TEXT,
            notes TEXT
        )
    ''')
    
    # Create performance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_performance (
            date DATE PRIMARY KEY,
            portfolio_value REAL,
            cash REAL,
            equity REAL,
            day_pl REAL,
            total_pl REAL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

# calculate_position_metrics(symbol):
def log_trade_to_db(symbol, side, quantity, price, strategy="manual", notes=""):
    """Log trade to SQLite database"""
    try:
        conn = sqlite3.connect('trading_log.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO trades (timestamp, symbol, side, quantity, price, total_value, strategy, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now(),
            symbol,
            side,
            quantity,
            price,
            quantity * price,
            strategy,
            notes
        ))
        
        conn.commit()
        conn.close()
        print(f"Trade logged to database: {side} {quantity} {symbol} @ ${price}")
    except Exception as e:
        print(f"Error logging trade to database: {e}")

# This function retrieves trade history from the local SQLite database for a specified number of past days.
def get_trade_history_from_db(days=30):
    """Get trade history from local database"""
    try:
        conn = sqlite3.connect('trading_log.db')
        query = '''
            SELECT * FROM trades 
            WHERE timestamp >= date('now', '-{} days')
            ORDER BY timestamp DESC
        '''.format(days)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching trade history from database: {e}")
        return pd.DataFrame()

# Initialize database on import
database_logger()