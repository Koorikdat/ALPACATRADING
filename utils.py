# utils.py
import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv

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
            print(u'\u2500' * 10)


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
    """
    Fetches OHLCV bar data from Alpaca's API for a given symbol.

    Args:
        symbol (str): The ticker symbol (e.g., "AAPL")
        timeframe (str): The time resolution (e.g., "1Min", "1Hour", "1Day")
        limit (int): Number of bars to retrieve
        show (bool): If True, prints the last 5 bars (optional)

    Returns:
        pd.DataFrame: A dataframe of historical bars
    """
    bars_df = api.get_bars(symbol, timeframe, limit=limit).df

    if show:
        print(f"--- Last 5 Bars for {symbol} ({timeframe}) ---")
        print(bars_df[['open', 'high', 'low', 'close', 'volume']].tail())
        print("-" * 40)
        print(u'\u2500' * 10)


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
        print(u'\u2500' * 10)

    except Exception as e:
        print(f"Error submitting buy order for {symbol}: {e}")
        return None
        print(u'\u2500' * 10)




# get_current_price("AAPL")
def get_current_price(ticker: str) -> float:
    try:
        latest_trade = api.get_latest_trade(ticker)
        return latest_trade.price
        print(u'\u2500' * 10)

    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
        return None
        print(u'\u2500' * 10)



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
        print(u'\u2500' * 10)
    except:
        return False
        print(u'\u2500' * 10)





