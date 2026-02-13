import boto3
import json
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TradingSignals')

def lambda_handler(event, context):
    """
    Combine price + sentiment data and save to DynamoDB
    """
    tickers = ['SPY', 'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA']
    timestamp = datetime.now().isoformat()
    results = []
    
    for ticker in tickers:
        try:
            # Get latest price data
            price_files = s3.list_objects_v2(
                Bucket='trading-signals-081130952147-kanishka',
                Prefix=f'price_data/daily/{ticker}/'
            )
            
            if 'Contents' in price_files and price_files['Contents']:
                latest_price_file = sorted(price_files['Contents'], 
                                          key=lambda x: x['LastModified'])[-1]
                
                price_obj = s3.get_object(
                    Bucket='trading-signals-081130952147-kanishka',
                    Key=latest_price_file['Key']
                )
                price_data = json.loads(price_obj['Body'].read())
                
                # Extract latest price
                if 'chart' in price_data and 'result' in price_data['chart']:
                    result = price_data['chart']['result'][0]
                    latest_price = result['meta']['regularMarketPrice']
                    
                    # Get sentiment data
                    sentiment_files = s3.list_objects_v2(
                        Bucket='trading-signals-081130952147-kanishka',
                        Prefix=f'sentiment_data/{ticker}/'
                    )
                    
                    sentiment_score = 0.0
                    if 'Contents' in sentiment_files and sentiment_files['Contents']:
                        latest_sentiment_file = sorted(sentiment_files['Contents'],
                                                      key=lambda x: x['LastModified'])[-1]
                        sent_obj = s3.get_object(
                            Bucket='trading-signals-081130952147-kanishka',
                            Key=latest_sentiment_file['Key']
                        )
                        sentiment_data = json.loads(sent_obj['Body'].read())
                        sentiment_score = sentiment_data.get('sentiment_score', 0.0)
                    
                    # Calculate combined signal (-1 to +1)
                    # Simple: average of price momentum + sentiment
                    combined_signal = sentiment_score  # For now, just use sentiment
                    
                    # Determine position: BUY (1), HOLD (0), SELL (-1)
                    if combined_signal > 0.2:
                        position = 'BUY'
                        position_value = 1
                    elif combined_signal < -0.2:
                        position = 'SELL'
                        position_value = -1
                    else:
                        position = 'HOLD'
                        position_value = 0
                    
                    # Save to DynamoDB
                    table.put_item(
                        Item={
                            'ticker': ticker,
                            'timestamp': timestamp,
                            'price': str(latest_price),
                            'sentiment_score': str(sentiment_score),
                            'combined_signal': str(combined_signal),
                            'position': position,
                            'position_value': position_value
                        }
                    )
                    
                    print(f"✅ {ticker}: ${latest_price}, Sentiment: {sentiment_score:.2f}, Signal: {position}")
                    results.append(f"{ticker} {position}")
            
        except Exception as e:
            print(f"❌ {ticker}: {e}")
            results.append(f"{ticker} ERROR")
    
    return {'statusCode': 200, 'body': json.dumps(results)}
