import boto3
import requests
import json
from datetime import datetime

s3 = boto3.client('s3')
FMP_API_KEY = 'xQgjx7M3mfg0dkjD8j925TydmGsoAX7s'

def lambda_handler(event, context):
    tickers = ['SPY', 'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        
        # Daily (2 years)
        url_daily = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={FMP_API_KEY}"
        resp = requests.get(url_daily, timeout=30)
        
        if resp.status_code == 200:
            data = resp.json()
            s3.put_object(
                Bucket='trading-signals-081130952147-kanishka',
                Key=f'price_data/daily/{ticker}/{timestamp}.json',
                Body=json.dumps(data)
            )
            print(f"✅ {ticker} daily ({len(data.get('historical', []))} rows)")
        
        # Intraday (30 days)
        end = datetime.now().strftime('%Y-%m-%d')
        start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        url_intraday = f"https://financialmodelingprep.com/api/v3/historical-chart/1min/{ticker}?from={start}&to={end}&apikey={FMP_API_KEY}"
        resp_intraday = requests.get(url_intraday, timeout=30)
        
        if resp_intraday.status_code == 200:
            s3.put_object(
                Bucket='trading-signals-081130952147-kanishka',
                Key=f'price_data/intraday/{ticker}/{timestamp}.json',
                Body=json.dumps(resp_intraday.json())
            )
            print(f"✅ {ticker} intraday")
    
    return {'statusCode': 200, 'body': 'SUCCESS - Data in S3'}
