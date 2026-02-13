# AWS Trading Signals Platform

A production-ready algorithmic trading signal generation system built on AWS.

## Features
- Real-time stock price data collection (Yahoo Finance)
- Sentiment analysis on financial news
- Automated signal generation (BUY/HOLD/SELL)
- Live dashboard with data visualization
- Fully automated with EventBridge scheduling

## AWS Services (10+)
- Lambda (3 functions)
- S3 (data lake)
- DynamoDB (signals database)
- EventBridge (scheduling)
- CloudWatch (monitoring)
- IAM (security)
- Streamlit (dashboard)

## Stocks Tracked
SPY, AAPL, MSFT, GOOGL, NVDA, TSLA

## Architecture
```
Yahoo Finance API
       ↓
Lambda (Price Data) → S3
       ↓
Lambda (Sentiment) → S3
       ↓
Lambda (Combine) → DynamoDB
       ↓
Streamlit Dashboard
```

## Results
- 6 stocks monitored
- Updates every 6 hours
- Real-time BUY/HOLD/SELL signals
- Sentiment + price analysis

Built in 1 day using AWS free tier credits.
