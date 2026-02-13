import boto3
import urllib.request
import csv
import io
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    tickers = ['SPY', 'QQL', 'AAPL', 'MSFT']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        
        # Download CSV directly from Yahoo (no yfinance needed)
        url_daily = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={int((datetime.now().timestamp() - 63072000))}&period2={int(datetime.now().timestamp())}&interval=1d&events=history"
        
        with urllib.request.urlopen(url_daily) as response:
            df_daily = csv.reader(io.StringIO(response.read().decode()))
            csv_content = '\n'.join(['+'.join(row) for row in df_daily])
            
            s3.put_object(
                Bucket='trading-signals-081130952147-kanishka',
                Key=f'price_data/daily/{ticker}/{timestamp}.csv',
                Body=csv_content
            )
    
    return {'statusCode': 200, 'body': 'Data ingested'}
