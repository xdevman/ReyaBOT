import requests
import json

from database2 import switch_alarm_status, update_order_id


def Get_Reya_api(wallet_address):
    
    url = f"https://api.reya.xyz/api/xp/user-leaderboard-v4-data/{wallet_address}"
    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
        
        # print(r.json())
    else:
        print(f"Request failed with status code {r.status_code}")

    liquidity_xp = data["liquidityXp"]
    total_xp = data["totalXp"]["value"]
    total_xp_sum = liquidity_xp + total_xp
    # print("Deposit: $", data['deposit'])
    # print("TradingXp: ", data['tradingXp'])
    # print(f"Calculated XP: {total_xp_sum:,.2f}")
    return {
        "deposit": data['deposit'],
        "tradingXp": data['tradingXp'],
        "Xp earned": total_xp_sum,
        "WeeklyRank": data['ranking'],
        "Rank":data["rank"]["rankName"]
    }



def format_price_data(entry):
    ticker = entry["ticker"].split("-")[0]  # Extract base asset (e.g., ETH, BTC, SOL)
    price = entry["markPrice"]
    price_change = entry["priceChange24HPercentage"]
    volume = entry["volume24H"]
    open_interest = entry["openInterest"]
    funding_rate = entry["fundingRate"] * 100  # Convert to percentage
    funding_rate_annualized = entry["fundingRateAnnualized"]
    
    price_change_symbol = "🚀" if price_change > 0 else "😕" if price_change < 0 else "😐"
    
    return f"""
{ticker}
${price:,.2f}
24h   {price_change:.2f}%   {price_change_symbol}
Vol: ${volume:,.2f} rUSD
OI: {open_interest:,.2f} {entry['quoteToken']}
Funding: {funding_rate:.4f}% / {funding_rate_annualized:.2f}% Annualized
""".strip()

def get_price(symbol):
    url = f"https://api.reya.xyz/api/markets/"
    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
    else:
        return f"Request failed with status code {r.status_code}" 
    symbol = symbol.upper()
    for entry in data:
        t = str(entry["ticker"]).upper()
        if t.startswith(symbol):
            return format_price_data(entry)
    return f"No data found for {symbol}"

def get_ticker_by_market_id(market_id):
    url = "https://api.reya.xyz/api/markets/"
    response = requests.get(url)
    
    if response.status_code == 200:
        markets = response.json()
        for market in markets:
            if str(market["id"]) == str(market_id):
                return market["ticker"]
        return None
    else:
        raise Exception(f"API Error: {response.status_code}")

def Get_orders(wallet_address):
    url = f"https://api.reya.xyz/api/accounts/{wallet_address}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"API Error: {response.status_code}")

def get_symbol(symbol):

    url = f"https://api.reya.xyz/api/markets/"
    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
    else:
        return None
    symbol = symbol.upper()
    for entry in data:
        t = str(entry["ticker"]).upper()
        if t.startswith(symbol):
            return entry["ticker"]
    return None

def save_latest_orderid(userid,wallet_address):
    result = switch_alarm_status(userid)
    print("switch alarm result : ", result)
    if result is True:
        url = f"https://api.reya.xyz/api/conditional-orders/get-orders-by-wallet/{wallet_address}"
        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()
            if len(data) == 0:
                return True
            
            print(data, data[0]["orderId"])
            result_orderid = update_order_id(userid, data[0]["orderId"])
            if result_orderid:
                return True
        else:
            return None
    else: 
        return False