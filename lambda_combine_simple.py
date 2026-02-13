import boto3
import json
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TradingSignals')

def lambda_handler(event, context):
    tickers = ['SPY', 'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA']
    timestamp = datetime.now().isoformat()
    results = []
    
    for ticker in tickers:
        try:
            # Simple: just save a test record to DynamoDB
            table.put_item(
                Item={
                    'ticker': ticker,
                    'timestamp': timestamp,
                    'price': '100.00',
                    'sentiment_score': '0.5',
                    'combined_signal': '0.5',
                    'position': 'BUY',
                    'position_value': 1
                }
            )
            
            print(f"✅ {ticker}: Test record saved")
            results.append(f"{ticker} OK")
            
        except Exception as e:
            print(f"❌ {ticker}: {e}")
            results.append(f"{ticker} ERROR: {str(e)}")
    
    return {'statusCode': 200, 'body': json.dumps(results)}
