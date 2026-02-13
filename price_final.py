import boto3
import urllib.request
import csv
import io
import time
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    tickers = ['SPY', 'AAPL']  # Start small
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        
        # 30 days daily data (smaller = less likely rate limited)
        start_time = int((datetime.now().timestamp() - 2592000))  # 30 days
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_time}&period2={int(datetime.now().timestamp())}&interval=1d&events=history"
        
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                csv_content = response.read().decode('utf-8')
                s3.put_object(
                    Bucket='trading-signals-081130952147-kanishka',
                    Key=f'price_data/daily/{ticker}/{timestamp}.csv',
                    Body=csv_content
                )
                print(f"✅ {ticker} saved")
        except Exception as e:
            print(f"❌ {ticker}: {str(e)}")
        
        time.sleep(5)  # 5 sec delay
    
    return {'statusCode': 200, 'body': 'Success'}
