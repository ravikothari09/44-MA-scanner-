import yfinance as yf
import requests

# =========================
# TELEGRAM SETTINGS
# =========================

BOT_TOKEN = "8856849594:AAFxxH1JNrf5ysRYOFUA6dfYg7b4FDFMZL8"
CHAT_ID = "454302134"

# =========================
# NIFTY 100 STOCKS
# =========================

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
'IDFCFIRSTB.NS','INDHOTEL.NS',
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
'SAIL.NS','SBIN.NS','SBICARD.NS',
'SBILIFE.NS','SHREECEM.NS','SHRIRAMFIN.NS',
'SIEMENS.NS','SUNPHARMA.NS','TATACONSUM.NS',
'TATAMOTORS.NS','TATAPOWER.NS','TATASTEEL.NS',
'TCS.NS','TECHM.NS','TITAN.NS',
'TORNTPHARM.NS','TRENT.NS','TVSMOTOR.NS',
'ULTRACEMCO.NS','UPL.NS','VEDL.NS',
'WIPRO.NS','ZOMATO.NS'

]

# =========================
# RESULT LISTS
# =========================

support = []
resistance = []

# =========================
# SCAN STOCKS
# =========================

for stock in stocks:

    try:

        print(f"Checking {stock}")

        df = yf.download(
            stock,
            period="6mo",
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        if df.empty:
            continue

        # 44 SMA
        df["SMA44"] = df["Close"].rolling(window=44).mean()

        latest_close = float(df["Close"].iloc[-1])
        latest_sma = float(df["SMA44"].iloc[-1])

        # Skip invalid SMA
        if latest_sma <= 0:
            continue

        # Distance from SMA
        distance = abs(latest_close - latest_sma) / latest_sma * 100

        stock_name = stock.replace(".NS", "")

        # Near SMA condition
        if distance <= 8:

            # Above SMA = support
            if latest_close >= latest_sma:

                support.append(
                    f"{stock_name} → {round(distance,2)}% above SMA44"
                )

            # Below SMA = resistance
            else:

                resistance.append(
                    f"{stock_name} → {round(distance,2)}% below SMA44"
                )

    except Exception as e:

        print(f"ERROR in {stock}: {e}")

# =========================
# TELEGRAM MESSAGE
# =========================

message = "📈 NIFTY 100 SMA44 SCAN\n\n"

message += "🟢 SUPPORT AREA\n"

if support:
    message += "\n".join(support)
else:
    message += "No Stocks"

message += "\n\n🔴 RESISTANCE AREA\n"

if resistance:
    message += "\n".join(resistance)
else:
    message += "No Stocks"

print(message)

# =========================
# SEND TELEGRAM MESSAGE
# =========================

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Message sent successfully!")
