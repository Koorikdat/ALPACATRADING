# Modular Algorithmic Trading Framework

### Paper Trading Infrastructure (Research-Oriented)

---

## Project Status

This project is currently paused due to brokerage API access limitations in Canada affecting the Alpaca paper trading environment.

The system architecture remains intact. A future iteration will migrate toward a broker-agnostic execution layer.

---

## Overview

This repository contains a modular algorithmic trading framework built for:

- Strategy prototyping
- Paper trade execution
- Portfolio inspection
- Risk-aware order placement
- Persistent trade logging
- Sentiment-based signal enrichment

The system is designed as infrastructure rather than a single-file trading bot.

---

## System Architecture

### Design Principles

- Separation of concerns
- Reusable execution layer
- Strategy abstraction
- Persistent logging independent of broker
- Broker replacement ready

---

## Project Structure

.
├── main.py
├── strats.py
├── utils.py
├── sentimentAnalysis.py
├── gui.py
├── trading_log.db
├── requirements.txt
└── .env



---

## Core Components

### main.py  
Orchestration layer.

Responsible for:
- Account validation
- Market open checks
- Strategy execution
- Portfolio display

---

### strats.py  
Strategy layer.

Example implemented:

`simple_algo(ticker, threshold)`

- Pulls recent intraday bars
- Extracts latest close
- Compares against threshold
- Triggers execution via utility layer

Strategies remain lightweight and depend on shared infrastructure.

---

### utils.py  
Core execution and data engine.

This is the workhorse of the codebase.

Includes:

Brokerage integration:
- Authentication
- Account status retrieval
- Order submission (market, limit, stop-loss)
- Order history retrieval

Market data:
- Historical OHLCV bars
- Latest trade retrieval
- Multi-symbol price queries
- Portfolio history

Portfolio and risk utilities:
- Position inspection
- Buying power checks
- Performance calculation
- Risk helpers

Persistence:
- SQLite database initialization
- Trade logging
- Historical trade retrieval
- Daily performance tracking

---

### sentimentAnalysis.py

Alternative data module.

- Extracts tickers from Reddit titles
- Scores sentiment (positive / neutral / negative)
- Provides compound sentiment metric

---

### gui.py

Tkinter interface prototype.

Current functionality:
- Manual ticker input
- Price retrieval using yfinance
- Simple display layer

Planned expansion:
- Portfolio monitoring
- Strategy state visualization
- Trade history viewer
- Risk exposure display

---

## Execution Flow

1. Load environment variables
2. Authenticate with broker
3. Validate account and market state
4. Pull market data
5. Generate signal
6. Execute order
7. Log trade
8. Update portfolio metrics

---

## Data Persistence

SQLite database: `trading_log.db`

Tables:

trades:
- Timestamp
- Symbol
- Side
- Quantity
- Price
- Strategy tag
- Notes

daily_performance:
- Portfolio value
- Cash
- Equity
- Daily PnL
- Cumulative PnL

---

## Planned Enhancements

- Broker abstraction interface
- Backtesting engine
- Event-driven architecture
- Parameter optimization framework
- Volatility-based position sizing
- Streaming data integration
- Structured logging

---

## Disclaimer

This project is for research and educational purposes only.

Paper trading results do not imply live trading performance.

No investment advice is provided.
