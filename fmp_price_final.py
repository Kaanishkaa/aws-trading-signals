import boto3
import requests
import pandas as pd
import io
from datetime import datetime, timedelta

s3 = boto3.client('s3')

# REPLACE WITH YOUR FMP API KEY
FMP_API_KEY = 'xQgjx7M3mfg0dkjD8j925TydmGsoAX7s'

def lambda_handler(event, context):
    tickers = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'META', 'JPM', 'GS']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        
        # Daily data (2 years)
        url_daily = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={FMP_API_KEY}"
        resp = requests.get(url_daily, timeout=30)
        
        if resp.status_code == 200:
            data = resp.json()
            if 'historical' in data and len(data['historical']) > 0:
                df_daily = pd.DataFrame(data['historical'])
                df_daily['date'] = pd.to_datetime(df_daily['date'])
                df_daily = df_daily.sort_values('date').set_index('date')
                
                csv_buffer = io.StringIO()
                df_daily.to_csv(csv_buffer)
                
                s3.put_object(
                    Bucket='trading-signals-081130952147-kanishka',
                    Key=f'price_data/daily/{ticker}/{timestamp}.csv',
                    Body=csv_buffer.getvalue()
                )
                print(f"✅ Saved {ticker} daily ({len(df_daily)} rows)")
        
        # Intraday (1 month, 1min)
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        url_intraday = f"https://financialmodelingprep.com/api/v3/historical-chart/1min/{ticker}?from={start_date}&to={end_date}&apikey={FMP_API_KEY}"
        
        resp = requests.get(url_intraday, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            if len(data) > 0:
                df_intraday = pd.DataFrame(data)
                df_intraday['date'] = pd.to_datetime(df_intraday['date'])
                df_intraday = df_intraday.sort_values('date').set_index('date')
                
                csv_buffer = io.StringIO()
                df_intraday.to_csv(csv_buffer)
                
                s3.put_object(
                    Bucket='trading-signals-081130952147-kanishka',
                    Key=f'price_data/intraday/{ticker}/{timestamp}.csv',
                    Body=csv_buffer.getvalue()
                )
                print(f"✅ Saved {ticker} intraday ({len(df_intraday)} rows)")
    
    return {'statusCode': 200, 'body': f'Data for {len(tickers)} tickers saved to S3'}
