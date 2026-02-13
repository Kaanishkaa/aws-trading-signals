# AWS Trading Signals Platform

A production-grade, multi-factor trading signal generation and backtesting system built on AWS, combining technical indicators, sentiment analysis, and real market data for interview-ready quant stories.

## 📊 Dashboard Preview

![Trading Signals Dashboard](screenshots/dashboard.png)
*Real-time trading signals with BUY/HOLD/SELL recommendations*

![Signal Distribution](screenshots/signals-chart.png)
*Combined signal strength visualization across all tracked stocks*

## 🎯 Overview

This platform generates systematic trading signals by combining:

Price data (OHLCV) from Yahoo Finance

Technical indicators (RSI, moving averages, Bollinger Bands, MACD)

Sentiment scores from financial news (FinBERT-style pipeline, mocked or notebook-based)

Multi-factor signal weighting and backtesting

The system monitors a basket of liquid names (e.g., SPY, AAPL, MSFT, GOOGL, NVDA, TSLA) and produces BUY/HOLD/SELL recommendations, portfolio metrics, and visual performance reports.

## ✨ Features

- **Real-time Data Collection** - Yahoo Finance API integration
- **Sentiment Analysis** - Financial news sentiment scoring
- **Automated Signal Generation** - BUY/HOLD/SELL recommendations
- **Live Dashboard** - Interactive data visualization
- **Fully Automated** - EventBridge scheduling (updates every 6 hours)

## 🏗️ Architecture
```
Yahoo Finance API
       ↓
Lambda (Price Data) → S3 Storage
       ↓
Lambda (Sentiment Analysis) → S3 Storage
       ↓
Lambda (Signal Combiner) → DynamoDB
       ↓
Streamlit Dashboard (Real-time Visualization)
```

## 🛠️ Technologies & Tools
**Languages & Libraries**

-Python (pandas, NumPy, requests)

-yfinance (price data)

-Plotly / Matplotlib (visualizations)

-Transformers / FinBERT-style pipeline for sentiment (notebook-based)

**AWS & Cloud**

-AWS Lambda (data ingestion, processing prototypes)

-Amazon S3 (data lake: raw price, news, processed features, backtest results)

-Amazon DynamoDB (latest signals, optional)

-Amazon EventBridge (scheduled runs / cron-style triggers)

-Amazon CloudWatch (logs, basic monitoring, alarms)

-AWS IAM (roles, policies, least-privilege access)

**Analytics & Dashboard**

-Streamlit (interactive dashboard)

-Jupyter / Colab notebooks (exploration, backtesting, sentiment experiments)

Architecture diagram (draw.io / diagrams.net)


## 🧩 Problems Faced & How They Were Solved

**Lambda packaging & dependencies**

Hit issues with scientific Python dependencies in the Lambda runtime

Solution: kept the core backtest + indicator logic in a notebook/EC2 environment; used Lambda mainly for ingestion and orchestration

**Pandas alignment & NaNs**

Encountered ValueError: operands are not aligned and KeyError on indicator columns

Solution: centralized indicator computation, enforced consistent indexes, and dropped/handled NaNs before signal generation

**API limits / data quality**

Dealt with API limits and occasional missing data from providers

Solution: added basic checks, retry logic where needed, and S3-based caching of downloaded data

**Cost & complexity**

Designed with serverless-first mindset to keep costs low and avoid over-engineering

Limited always-on components; leaned on scheduled jobs and notebooks where appropriate

## 📊 Results

- **6 stocks monitored**: SPY, AAPL, MSFT, GOOGL, NVDA, TSLA
- **Data updates**: Every 6 hours (automated)
- **Signal types**: BUY, HOLD, SELL
- **Metrics tracked**: Price, Sentiment Score, Combined Signal

## 🎓 Skills Demonstrated

- AWS Cloud Architecture
- Serverless Computing (Lambda)
- NoSQL Databases (DynamoDB)
- Data Engineering (S3 Data Lake)
- Machine Learning (Sentiment Analysis)
- Event-Driven Architecture
- Dashboard Development (Streamlit)

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 👤 Author

**Kaanishkaa**
- GitHub: [@Kaanishkaa](https://github.com/Kaanishkaa)

---


