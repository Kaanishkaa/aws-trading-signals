import boto3
import requests
import json
from datetime import datetime

s3 = boto3.client('s3')
FMP_API_KEY = 'demo'  # REPLACE 'demo' WITH YOUR FMP KEY

def lambda_handler(event, context):
    tickers = ['SPY', 'AAPL', 'MSFT']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        
        # FMP daily (2 years)
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={FMP_API_KEY}"
        resp = requests.get(url, timeout=30)
        
        if resp.status_code == 200:
            data = resp.json()
            if 'historical' in data:
                # Save raw JSON to S3 (no pandas needed)
                s3.put_object(
                    Bucket='trading-signals-081130952147-kanishka',
                    Key=f'price_data/daily/{ticker}/{timestamp}.json',
                    Body=json.dumps(data)
                )
                print(f"✅ {ticker} daily saved")
        
        # Intraday
        url_intraday = f"https://financialmodelingprep.com/api/v3/historical-chart/1min/{ticker}?from=2026-01-12&to=2026-02-11&apikey={FMP_API_KEY}"
        resp = requests.get(url_intraday)
        if resp.status_code == 200:
            s3.put_object(
                Bucket='trading-signals-081130952147-kanishka',
                Key=f'price_data/intraday/{ticker}/{timestamp}.json',
                Body=json.dumps(resp.json())
            )
            print(f"✅ {ticker} intraday saved")
    
    return {'statusCode': 200, 'body': 'Data saved to S3'}
