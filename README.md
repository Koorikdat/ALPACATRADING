Modular Algorithmic Trading Framework (Paper Trading)
Status

This project is currently paused due to brokerage API access limitations in Canada affecting the Alpaca paper trading environment.

The architecture and infrastructure remain intact. Future iterations will migrate toward a broker-agnostic execution layer.

Summary

This project is a modular algorithmic trading framework designed for:

Strategy prototyping

Paper trade execution

Portfolio state inspection

Risk-aware order placement

Persistent trade logging

Sentiment-based signal integration

The system was built with separation of concerns in mind: execution logic, strategy logic, data access, and persistence are deliberately decoupled.

This is infrastructure-first design, not a single-script trading bot.

System Design
Architectural Principles

Modular decomposition of trading components

Reusable execution and data utilities

Clear separation between signal generation and order execution

Persistent logging independent of broker

Designed for eventual broker abstraction

Project Structure
.
├── main.py                # Orchestration layer
├── strats.py              # Strategy definitions
├── utils.py               # Core execution + data layer
├── sentimentAnalysis.py   # Signal enrichment module
├── gui.py                 # Dashboard prototype
├── trading_log.db         # Local SQLite store
├── requirements.txt
└── .env

Core Modules
main.py — Orchestration Layer

Validates account state and market status

Executes strategy functions

Handles execution sequencing

Displays portfolio state before/after actions

Acts as the runtime controller.

strats.py — Strategy Layer

Defines signal logic.

Example included:

simple_algo(ticker, threshold)

Pulls recent intraday bars

Compares last price to threshold

Triggers execution through utility layer

Strategies remain intentionally lightweight and depend on reusable infrastructure.

This allows:

Rapid strategy iteration

Parameter experimentation

Easy extension to multiple models

utils.py — Core Engine (Execution + Data Layer)

This is the backbone of the system.

It encapsulates:

Brokerage Integration

Authentication

Account status retrieval

Market clock checks

Order submission (market, limit, stop-loss)

Market Data Access

Historical OHLCV bars

Latest trade retrieval

Multi-symbol price queries

Portfolio history

Portfolio & Risk Utilities

Position inspection

Performance calculation over time windows

Buying power checks

Risk assessment helpers

Persistence Layer

Automatic SQLite database initialization

Trade logging

Historical trade retrieval

Daily performance storage

The goal is to isolate external dependencies and keep strategy code free of API-specific details.

sentimentAnalysis.py — Signal Enrichment

Implements lightweight sentiment scoring using VADER.

Features:

Ticker extraction from Reddit post titles

Sentiment classification (positive / neutral / negative)

Compound sentiment scoring

Designed to augment price-based signals with alternative data inputs.

gui.py — Interface Prototype

Built with Tkinter.

Current functionality:

Manual ticker input

Price retrieval using yfinance

Basic display layer

Future goal: evolve into a monitoring dashboard for:

Portfolio metrics

Strategy state

Trade logs

Risk exposure

Data Persistence

The system maintains a local SQLite database:

trades

Stores:

Timestamp

Symbol

Side

Quantity

Execution price

Strategy tag

Notes

daily_performance

Stores:

Portfolio value

Cash

Equity

Daily P&L

Cumulative P&L

This enables offline analytics independent of broker dashboards.

Execution Flow

Load environment variables

Authenticate with brokerage

Validate account state and market open status

Pull market data

Generate signal

Execute order

Log trade

Update portfolio state

Design Considerations

Designed for extension into broker-agnostic execution

Modular structure supports backtesting integration

Logging enables auditability

Risk logic separated from signal logic

Database persistence allows historical analytics

Planned Enhancements

Broker abstraction layer (interface pattern)

Event-driven architecture

Backtesting engine integration

Strategy parameter optimization

Improved risk engine (position sizing, volatility targeting)

Streaming data support

Structured logging and monitoring

Disclaimer

This project is for research and educational purposes only.
Paper trading performance does not imply live trading performance.
No investment advice is provided.
