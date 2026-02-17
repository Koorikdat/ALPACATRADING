Modular Algorithmic Trading Framework
Paper Trading Infrastructure (Research-Oriented)
⚠ Project Status

This project is currently paused due to brokerage API access limitations in Canada affecting the Alpaca paper trading environment.

The system architecture remains fully intact. Future iterations will migrate toward a broker-agnostic execution layer.

Overview

This repository contains a modular algorithmic trading framework built for:

Strategy prototyping

Paper trade execution

Portfolio state inspection

Risk-aware order placement

Persistent trade logging

Sentiment-based signal enrichment

The design emphasizes infrastructure over scripting.

This is not a single-file trading bot — it is structured as a layered system.

System Architecture
Design Principles

Separation of concerns

Reusable execution layer

Strategy abstraction

Persistent logging independent of broker

Designed for broker replacement

Project Structure
.
├── main.py                # Orchestration layer
├── strats.py              # Strategy definitions
├── utils.py               # Core execution + data layer
├── sentimentAnalysis.py   # Signal enrichment
├── gui.py                 # Dashboard prototype
├── trading_log.db         # SQLite persistence
├── requirements.txt
└── .env

Core Components
1. main.py
Orchestration Layer

Responsible for runtime control:

Validates account state

Checks market open/close status

Executes strategy logic

Displays portfolio state before and after actions

Acts as the execution controller of the system.

2. strats.py
Strategy Layer

Defines signal-generation logic.

Example implemented:

simple_algo(ticker, threshold)

Pulls recent intraday bars

Extracts latest close

Compares against threshold

Triggers execution via utility layer

Strategies remain intentionally lightweight and depend on infrastructure from utils.py.

This allows:

Rapid iteration

Clean experimentation

Strategy isolation from API logic

3. utils.py
Core Engine (Execution + Data Layer)

This is the workhorse of the codebase.

It encapsulates nearly all system functionality.

Brokerage Integration

Authentication

Account status retrieval

Market clock validation

Order submission (market, limit, stop-loss)

Order history retrieval

Market Data Access

Historical OHLCV bars

Latest trade retrieval

Multi-symbol price queries

Portfolio history

Portfolio & Risk Utilities

Position inspection

Buying power checks

Performance calculation over rolling windows

Risk assessment helpers

Persistence Layer (SQLite)

Automatic database initialization

Trade logging

Historical trade retrieval

Daily performance tracking

By centralizing these functions, strategy logic remains clean and portable.

4. sentimentAnalysis.py
Alternative Data Module

Implements lightweight sentiment scoring using VADER.

Capabilities:

Extracts tickers from Reddit post titles

Classifies sentiment (positive / neutral / negative)

Produces compound sentiment scores

Designed to augment price-based strategies with alternative signals.

5. gui.py
Interface Prototype

Built with Tkinter.

Current functionality:

Manual ticker input

Price retrieval via yfinance

Simple display layer

Future goal:

Portfolio monitoring dashboard

Strategy state visualization

Trade history viewer

Risk exposure display

Execution Flow

Load environment variables

Authenticate with broker

Validate account + market state

Pull market data

Generate signal

Execute order

Log trade to database

Update portfolio metrics

Data Persistence

A local SQLite database (trading_log.db) stores:

trades

Timestamp

Symbol

Side

Quantity

Execution price

Strategy tag

Notes

daily_performance

Portfolio value

Cash

Equity

Daily P&L

Cumulative P&L

This enables offline analytics independent of broker dashboards.

Technical Focus Areas

Modular system design

Strategy/execution separation

Persistent state management

API abstraction readiness

Lightweight alternative data integration

Planned Enhancements

Broker abstraction interface

Event-driven architecture

Backtesting engine integration

Parameter optimization framework

Volatility-based position sizing

Streaming data integration

Structured logging + monitoring

Disclaimer

This project is for research and educational purposes only.
Paper trading results do not imply live trading performance.
No investment advice is provided.
