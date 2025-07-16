Project for testing algorithmic tradic algorithms using the ALPACA system.




main.py

    This will determine the main logic of the software, it will allow us to call functions from the other modules

strats.py

    This will contain the trading strategies, we can decide here what our behaviour will be

utils.py

    This contains functions that will allow us to interact with our portfolio (buy/sell) as well as general api calls from the trading platform

sentimentAnalysis.py

    The goal here is to be able to scrape websites to determine sentiment on a given stock, perhaps returning a score


.venv + requirements.txt + .env

    These set up the environment and make usage work. ensures compatibility and allows secure API calls.

gui.py

    This will eventually be a dashboard that will allow interaction and display inportant information