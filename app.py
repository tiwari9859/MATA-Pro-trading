import streamlit as st
import yfinance as yf

st.title("📈 M.A.T.A Pro - AI Trading Tool")

ticker = st.sidebar.text_input("Enter Asset", "BTC-USD")

data = yf.download(ticker, period="1mo", interval="1d")

st.subheader("Price Chart")
st.line_chart(data['Close'])

# Button dabane par processing dikhega aur fir hat jayega
if st.button("Analyze Now"):
    with st.spinner('Processing... AI Model Active!'):
        # Yahan aap apna AI analysis ka code baad mein daal sakte hain
        st.success('Analysis Complete!')
