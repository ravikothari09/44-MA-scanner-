import yfinance as yf
import pandas as pd
import requests

BOT_TOKEN = "8856849594:AAFxxH1JNrf5ysRYOFUA6dfYg7b4FDFMZL8"
CHAT_ID = "454302134"

stocks = [
'ABB.NS','ABCAPITAL.NS','ABFRL.NS','ACC.NS',
'ADANIENT.NS','ADANIGREEN.NS','ADANIPORTS.NS',
'ALKEM.NS','AMBUJACEM.NS','APOLLOHOSP.NS',
'APOLLOTYRE.NS','ASHOKLEY.NS','ASIANPAINT.NS',
'ASTRAL.NS','ATGL.NS','AUBANK.NS',
'AUROPHARMA.NS','AXISBANK.NS','BAJAJ-AUTO.NS',
'BAJFINANCE.NS','BAJAJFINSV.NS','BANDHANBNK.NS',
'BANKBARODA.NS','BEL.NS','BERGEPAINT.NS',
'BHARATFORG.NS','BHARTIARTL.NS','BHEL.NS',
'BIOCON.NS','BPCL.NS','BRITANNIA.NS',
'CANBK.NS','CHOLAFIN.NS','CIPLA.NS',
'COALINDIA.NS','DABUR.NS','DIVISLAB.NS',
'DLF.NS','DRREDDY.NS','EICHERMOT.NS',
'GAIL.NS','GLAND.NS','GODREJCP.NS',
'GRASIM.NS','HAL.NS','HAVELLS.NS',
'HCLTECH.NS','HDFCBANK.NS','HDFCLIFE.NS',
'HEROMOTOCO.NS','HINDALCO.NS','HINDUNILVR.NS',
'ICICIBANK.NS','ICICIGI.NS','ICICIPRULI.NS',
'IDEA.NS','IDFCFIRSTB.NS','INDHOTEL.NS',
'INDIGO.NS','INDUSINDBK.NS','INFY.NS',
'IOC.NS','IRCTC.NS','ITC.NS',
'JINDALSTEL.NS','JSWSTEEL.NS','JUBLFOOD.NS',
'KOTAKBANK.NS','LT.NS','LTIM.NS',
'M&M.NS','MARICO.NS','MARUTI.NS',
'MCDOWELL-N.NS','MOTHERSON.NS','NAUKRI.NS',
'NESTLEIND.NS','NHPC.NS','NMDC.NS',
'NTPC.NS','OBEROIRLTY.NS','ONGC.NS',
'PAGEIND.NS','PAYTM.NS','PEL.NS',
'PETRONET.NS','PIDILITIND.NS','PNB.NS',
'POWERGRID.NS','RECLTD.NS','RELIANCE.NS',
'SAIL.NS','SBI.NS','SBICARD.NS',
'SBILIFE.NS','SHREECEM.NS','SHRIRAMFIN.NS',
'SIEMENS.NS','SUNPHARMA.NS','TATACONSUM.NS',
'TATAMOTORS.NS','TATAPOWER.NS','TATASTEEL.NS',
'TCS.NS','TECHM.NS','TITAN.NS',
'TORNTPHARM.NS','TRENT.NS','TVSMOTOR.NS',
'ULTRACEMCO.NS','UPL.NS','VEDL.NS',
'WIPRO.NS','ZOMATO.NS'
]
support = []
resistance = []

for stock in stocks:

    try:

        df = yf.download(stock, period="4mo", interval="1d")

        df['SMA44'] = df['Close'].rolling(44).mean()

        latest = df.iloc[-1]

        close = latest['Close']
        open_price = latest['Open']
        high = latest['High']
        low = latest['Low']
        sma44 = latest['SMA44']

        distance = abs(close - sma44) / sma44 * 100

        bullish = close > open_price
        bearish = close < open_price

        if distance <= 1.5:

            if close > sma44 and low <= sma44 and bullish:
                support.append(stock.replace(".NS",""))

            elif close < sma44 and high >= sma44 and bearish:
                resistance.append(stock.replace(".NS",""))

    except:
        pass

message = "📈 NIFTY SMA44 SCAN\n\n"

message += "🟢 SUPPORT ZONE\n"

if support:
    message += "\n".join(support)
else:
    message += "No Stocks"

message += "\n\n🔴 RESISTANCE ZONE\n"

if resistance:
    message += "\n".join(resistance)
else:
    message += "No Stocks"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message
})
