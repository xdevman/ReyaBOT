import requests
import json


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
        if entry["ticker"].startswith(symbol):
            return format_price_data(entry)
    return f"No data found for {symbol}"
