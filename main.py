import requests
from datetime import datetime
from telegram import Bot
import os

TOKEN = os.getenv("8517566632:AAHI-Avrutc5SgmGhi-pLV_7Vc7TtaatEzI")
CHAT_ID = os.getenv("7092256542")

bot = Bot(token=TOKEN)

symbols = ["BTCUSDT", "ETHUSDT"]

def get_price(symbol):
    url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
    return float(requests.get(url).json()["price"])

print("Bot Running...")

for sym in symbols:
    price = get_price(sym)

    msg = f"""
🚀 Crypto Alert

Coin: {sym}
Price: {price}
Time: {datetime.now().strftime("%H:%M:%S")}
"""

    bot.send_message(chat_id=CHAT_ID, text=msg)
