import streamlit as st
import boto3
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Trading Signals Dashboard", layout="wide")

# AWS clients
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

st.title("🏦 AWS Trading Signals Platform")
st.markdown("Real-time trading signals combining price data + sentiment analysis")

# Fetch latest signals from DynamoDB
@st.cache_data(ttl=300)
def get_latest_signals():
    table = dynamodb.Table('TradingSignals')
    response = table.scan()
    items = response.get('Items', [])
    if items:
        df = pd.DataFrame(items)
        # Get latest for each ticker
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        latest = df.sort_values('timestamp').groupby('ticker').last().reset_index()
        return latest
    return pd.DataFrame()

# Display current signals
st.header("📊 Current Trading Signals")

signals_df = get_latest_signals()

if not signals_df.empty:
    col1, col2, col3 = st.columns(3)
    
    for i, row in signals_df.iterrows():
        col = [col1, col2, col3][i % 3]
        
        with col:
            if row['position'] == 'BUY':
                st.success(f"**{row['ticker']}** - {row['position']}")
            elif row['position'] == 'SELL':
                st.error(f"**{row['ticker']}** - {row['position']}")
            else:
                st.info(f"**{row['ticker']}** - {row['position']}")
            
            st.metric("Price", f"${float(row['price']):.2f}")
            st.metric("Sentiment", f"{float(row['sentiment_score']):.2f}")
            st.metric("Signal", f"{float(row['combined_signal']):.2f}")
else:
    st.warning("No signals available yet. Run the combine Lambda function to generate signals.")

# Display signal distribution
if not signals_df.empty:
    st.header("📈 Signal Distribution")
    
    fig = go.Figure(data=[
        go.Bar(
            x=signals_df['ticker'],
            y=signals_df['combined_signal'].astype(float),
            marker_color=['green' if float(x) > 0 else 'red' for x in signals_df['combined_signal']]
        )
    ])
    
    fig.update_layout(
        title="Combined Signal Strength by Ticker",
        xaxis_title="Ticker",
        yaxis_title="Signal Strength",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

# System Status
st.header("⚙️ System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Lambda Functions", "3", "Active")
    
with col2:
    st.metric("Data Points", len(signals_df) if not signals_df.empty else 0)
    
with col3:
    st.metric("Last Update", datetime.now().strftime("%H:%M:%S"))

# Raw data view
with st.expander("🔍 View Raw Signal Data"):
    if not signals_df.empty:
        st.dataframe(signals_df, use_container_width=True)
    else:
        st.info("No data available")

st.markdown("---")
st.caption("Built with AWS Lambda, S3, DynamoDB, EventBridge | Data updates every 6 hours")
