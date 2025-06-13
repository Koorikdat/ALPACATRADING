from utils import *
from strats import *
import time
import time



def preliminary():
    """
    Checks if the account is active and if the market is currently open.
    Prints the current AAPL price if conditions are met.
    Returns True if ready to proceed, otherwise False.ß
    """
    status = get_account_status()
    
    if status != "ACTIVE":
        print(f"Account status is '{status}', cannot proceed")
        return False

    # Check market status using Alpaca clock
    try:
        clock = api.get_clock()
        if not clock.is_open:
            print("Market is closed — cannot place live orders")
            return False
    
        
    except Exception as e:
        print(f"Error checking market status: {e}")
        return False
    
    return True

    

def cancel_all_open_orders():
    print("Checking for open orders...")
    orders = api.list_orders(status='open')
    if not orders:
        print("No open orders to cancel.")
        return
    for order in orders:
        api.cancel_order(order.id)
    print(f"Cancelled {len(orders)} open order(s).")






def main():

    get_positions(True)

    print("______________________________________________________________________________________________________")
    balance = get_account_balance()
    print("______________________________________________________________________________________________________")
    

    # Ensure all pre-checks are met
    if not preliminary():
        return  # Stop script if account is inactive or market is closed
    
    buy_stock('AAPL', 1)

    print("______________________________________________________________________________________________________")
    balance = get_account_balance()
    print("______________________________________________________________________________________________________")

    get_positions(True)







if __name__ == "__main__":
    main()


