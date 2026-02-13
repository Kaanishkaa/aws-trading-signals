import boto3
import json
from datetime import datetime, timedelta
import urllib.request
import time

s3 = boto3.client('s3')

def lambda_handler(event, context):
    tickers = ['SPY', 'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = []

    for ticker in tickers:
        print(f"📊 Fetching {ticker}...")
        
        try:
            # Yahoo Finance with proper headers
            period1 = int((datetime.now() - timedelta(days=730)).timestamp())
            period2 = int(datetime.now().timestamp())
            
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={period1}&period2={period2}&interval=1d"
            
            # Add user agent to avoid rate limiting
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                }
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())
                
                # Save to S3
                s3.put_object(
                    Bucket='trading-signals-081130952147-kanishka',
                    Key=f'price_data/daily/{ticker}/{timestamp}.json',
                    Body=json.dumps(data)
                )
                
                num_points = len(data['chart']['result'][0]['timestamp'])
                print(f"✅ {ticker} saved ({num_points} days)")
                results.append(f"{ticker} OK")
                
            # Wait 2 seconds between requests to avoid rate limiting
            time.sleep(2)
                
        except Exception as e:
            print(f"❌ {ticker}: {e}")
            results.append(f"{ticker} ERROR")
    
    return {'statusCode': 200, 'body': json.dumps(results)}
