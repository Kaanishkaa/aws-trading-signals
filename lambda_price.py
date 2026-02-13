import yfinance as yf
import boto3
import json
import io
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    tickers = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'META', 'JPM', 'GS']
    
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        df_daily = yf.download(ticker, period='2y', interval='1d')
        df_intraday = yf.download(ticker, period='30d', interval='5m')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        csv_buffer = io.StringIO()
        df_daily.to_csv(csv_buffer)
        s3.put_object(Bucket='trading-signals-081130952147-kanishka', Key=f'price_data/daily/{ticker}/{timestamp}.csv', Body=csv_buffer.getvalue())
        
        csv_buffer = io.StringIO()
        df_intraday.to_csv(csv_buffer)
        s3.put_object(Bucket='trading-signals-081130952147-kanishka', Key=f'price_data/intraday/{ticker}/{timestamp}.csv', Body=csv_buffer.getvalue())
    
    return {'statusCode': 200, 'body': json.dumps('Data ingested successfully')}
