from reya_data_feed.consumer import ReyaSocket
import asyncio
import os
from dotenv import load_dotenv
from examples.utils.consts import MarketPriceStreams

def on_error(_, message):
    print("Error:", message)
    return None

def on_message_prices(ws: ReyaSocket, message: dict, currency_symbol, future):
    if message["type"] == "connected":
        ws.prices.subscribe(id=MarketPriceStreams[currency_symbol].value)
    
    if message["type"] == "channel_data" and message["id"] == MarketPriceStreams[currency_symbol].value:
        price = message["contents"].get("spotPrice")
        future.set_result(price)
        ws.close()

def get_crypto_price(currency_symbol: str):
    currency_symbol = currency_symbol.upper()
    
    if currency_symbol not in MarketPriceStreams.__members__:
        raise ValueError(f"Error: {currency_symbol} is not a valid market symbol!")
    
    load_dotenv()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = loop.create_future()
    
    ws = ReyaSocket(
        os.environ['REYA_WS_URL'],
        on_error=on_error,
        on_message=lambda ws, msg: on_message_prices(ws, msg, currency_symbol, future)
    )
    
    async def connect_and_wait():
        await ws.connect()
        return await future
    
    return loop.run_until_complete(connect_and_wait())

if __name__ == "__main__":
    currency = input("Enter currency symbol (e.g., BTC, ETH, SOL): ")
    try:
        price = get_crypto_price(currency)
        print(f"Current price of {currency}: {price}")
    except ValueError as e:
        print(e)
