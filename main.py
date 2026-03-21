import os
import requests
from datetime import datetime
from telegram import Bot
import asyncio

def send_telegram_message(token, chat_id, message):
    """Send a message via Telegram"""
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')

def fetch_crypto_price(symbol):
    """Fetch live crypto price from Binance Futures API"""
    try:
        url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def format_message(coin_name, price, symbol):
    """Format the Telegram message"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = (
        f"<b>💰 Crypto Alert</b>\n\n"
        f"<b>Coin:</b> {coin_name}\n"
        f"<b>Symbol:</b> {symbol}\n"
        f"<b>Price:</b> ${price:.2f}\n"
        f"<b>Time:</b> {current_time}"
    )
    return message

def main():
    """Main bot execution"""
    # Read environment variables
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    
    if not telegram_token or not chat_id:
        print("Error: TELEGRAM_TOKEN or CHAT_ID not set")
        return
    
    # Crypto coins to monitor
    coins = {
        'BTCUSDT': 'Bitcoin',
        'ETHUSDT': 'Ethereum',
        'SOLUSDT': 'Solana'
    }
    
    print("Fetching crypto prices...")
    
    # Fetch and send prices for each coin
    for symbol, coin_name in coins.items():
        price = fetch_crypto_price(symbol)
        
        if price is not None:
            message = format_message(coin_name, price, symbol)
            print(f"Sending message for {coin_name}...")
            
            try:
                asyncio.run(send_telegram_message(telegram_token, chat_id, message))
                print(f"✓ Message sent for {coin_name}")
            except Exception as e:
                print(f"✗ Failed to send message for {coin_name}: {e}")
        else:
            print(f"✗ Could not fetch price for {symbol}")
    
    print("Done!")

if __name__ == "__main__":
    main()
