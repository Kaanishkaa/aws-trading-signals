import boto3
import json
from datetime import datetime
import urllib.request
import urllib.parse

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Fetch news headlines and analyze sentiment
    Using NewsAPI for headlines
    """
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'SPY']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # For now, we'll use a simple keyword-based sentiment
    # (We'll upgrade to FinBERT in next step)
    
    results = []
    
    for ticker in tickers:
        try:
            # Fetch news from a free API (using Google News RSS)
            query = urllib.parse.quote(f"{ticker} stock")
            url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                news_data = response.read().decode()
                
                # Simple sentiment: count positive vs negative words
                positive_words = ['surge', 'gain', 'profit', 'beat', 'growth', 'high', 'up']
                negative_words = ['fall', 'loss', 'miss', 'decline', 'low', 'down', 'drop']
                
                pos_count = sum(1 for word in positive_words if word in news_data.lower())
                neg_count = sum(1 for word in negative_words if word in news_data.lower())
                
                sentiment_score = (pos_count - neg_count) / max(pos_count + neg_count, 1)
                
                sentiment = {
                    'ticker': ticker,
                    'timestamp': timestamp,
                    'sentiment_score': sentiment_score,
                    'positive_mentions': pos_count,
                    'negative_mentions': neg_count,
                    'news_count': news_data.count('<item>')
                }
                
                # Save to S3
                s3.put_object(
                    Bucket='trading-signals-081130952147-kanishka',
                    Key=f'sentiment_data/{ticker}/{timestamp}.json',
                    Body=json.dumps(sentiment)
                )
                
                print(f"✅ {ticker} sentiment: {sentiment_score:.2f}")
                results.append(f"{ticker} OK")
                
        except Exception as e:
            print(f"❌ {ticker}: {e}")
            results.append(f"{ticker} ERROR")
    
    return {'statusCode': 200, 'body': json.dumps(results)}
