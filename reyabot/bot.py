#!/usr/bin/python

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv
# from rsdk import cprice
from rapi import Get_Reya_api,get_price,Get_orders, get_ticker_by_market_id
from database2 import *
from elixir_api import update_elixir_rank

load_dotenv()

# Read values from .env
TOKEN = os.getenv("TOKEN")
# DEVELOP_TOKEN = "1144997276:AAFE8NBV0yKJkG8vs6BnBtmeP5_xWRZk2HI"
PROXY_ENABLED = os.getenv("PROXY_ENABLED", "False").lower() == "True"
PROXY = os.getenv("PROXY")

# Apply proxy if enabled
# if PROXY_ENABLED and PROXY:
#     apihelper.proxy = {"https": PROXY}

# Initialize bot
bot = telebot.TeleBot(TOKEN)

# start و help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    add_new_user(user_id)
    bot.reply_to(message, "Welcome! Use /price [coin] to get price info.")


@bot.message_handler(commands=['price','p'])
def send_price(message):
    args = message.text.split()  # Split message text
    if len(args) == 1:  # If just /price is used
        # pricex = cprice("BTC") Get price from websocket
        pricex = get_price("BTC")
        # bot.reply_to(message, f"*BTC*\n`$ {float(pricex):.2f}`\n\n[🚀 Trade on reya dex](https://app.reya.xyz/?referredBy=q4b99uc9)", parse_mode="Markdown")
        bot.reply_to(message, f"{pricex}\n\n[🚀 Trade on reya dex](https://app.reya.xyz/?referredBy=q4b99uc9)", parse_mode="Markdown")

    else:
        coin = args[1].upper()  # Convert input to uppercase
        # pricex = cprice(coin)
        pricex = get_price(coin)
        # bot.reply_to(message, f"*{coin}*\n`$ {float(pricex):.2f}`\n\n[🚀 Trade on reya dex](https://app.reya.xyz/?referredBy=q4b99uc9)", parse_mode="Markdown")
        bot.reply_to(message, f"{pricex}\n\n[🚀 Trade on reya dex](https://app.reya.xyz/?referredBy=q4b99uc9)", parse_mode="Markdown")


@bot.message_handler(commands=['positions'])
def open_orders(message):
    user_id = message.from_user.id
    try:
        addr_result = get_wallet_address(user_id)

        print("addr: ",addr_result)

        if addr_result == "null":
            bot.reply_to(message, "Wallet address not implemented. Please use /address to add your wallet address.")


        account_orders = Get_orders(addr_result)[0]["positions"] # Receive open orders from this address
        if not account_orders:
            bot.reply_to(message, "❌ No open positions.")
        else:
            all_positions = []
            for positions in account_orders:
                market_symbol = get_ticker_by_market_id(positions['marketId'])
                formatted_message = (

                    "*OPEN ORDERS*\n"
                    
                    f"🪙 *Market*: {market_symbol}\n"
                    f"📈 *LONG/SHORT*: {positions['side'].upper()}\n"
                    f"🏷️ *Entry Price*: {positions['price']:.4f}\n"
                    f"📊 *Live PnL*: {positions['livePnL']:.2f}\n"
                    f"🚨 *Liq. Price*:  {positions['liquidationPrice']:.4f}\n"
                    "---------------------\n"

                    )
                all_positions.append(formatted_message)
            final_message = "\n".join(all_positions)
            bot.reply_to(message, formatted_message, parse_mode='Markdown')

    except Exception as e:
        print("except Error",e)
        bot.reply_to(message,"Bot updated! Please type /start again to continue using it",)



@bot.message_handler(commands=['address'])
def set_address(message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) == 1:
        bot.reply_to(message,  f"Enter valid address")
    else:
        addr = args[1].lower() #get Wallet address and convert to lower case
        try:
            add_wallet_address(user_id,addr)
            bot.reply_to(message, f"Your wallet address has been saved: {addr}")
        except Exception as e:
            bot.reply_to(message, f"An error occurred while saving your wallet address: {str(e)}")
            
@bot.message_handler(commands=['elixir'])
def set_address(message):
    user_id = message.from_user.id
    args = message.text.split()

    
    if len(args) == 1:
        set_elixir_username(user_id, None)
        bot.reply_to(message, "✅ Your Elixir username has been removed.")
    
    else:
        addr = args[1].lower() #get username and convert to lower case
        try:
            set_elixir_username(user_id,addr)
            bot.reply_to(message, f"Your username has been saved: {addr}")
        except Exception as e:
            bot.reply_to(message, f"An error occurred while saving your username: {str(e)}")



@bot.message_handler(commands=['leaderboard'])
def get_leaderboard(message):
    user_id = message.from_user.id
    try:
        addr_result = get_wallet_address(user_id)

        print("addr: ",addr_result)

        if addr_result == "null":
            bot.reply_to(message, "Wallet address not implemented. Please use /address to add your wallet address.")

        else:
            XpData = Get_Reya_api(addr_result) #Get Xp Data
            elixir_data = update_elixir_rank(user_id)
            print("elixir_data:",elixir_data)
            formatted_message = (
        "*Leaderboard*\n"
        "---------------------\n"
        f"💰 *Deposit*: {XpData['deposit']:.2f}\n"
        f"📊 *Trading XP*: {XpData['tradingXp']}\n"
        f"🏆 *XP Earned*: {XpData['Xp earned']:,.2f}\n"
        f"🏆 *Weekly Rank*: {XpData['WeeklyRank']} *{XpData['Rank']}*\n"
        f"🏆 *Elixir Rank*: {elixir_data}\n"
        "---------------------\n"
        "Keep up the great work!"
    )
            bot.reply_to(message, formatted_message, parse_mode='Markdown')

    except Exception as e:
        print("except Error",e)
        bot.reply_to(message,"Bot updated! Please type /start again to continue using it",)


@bot.message_handler(commands=['links'])
def send_links(message):
    
    markup = InlineKeyboardMarkup()
    
    markup.add(InlineKeyboardButton("📢 Twitter", url="https://twitter.com/reya_xyz"))
    markup.add(InlineKeyboardButton("📖 Docs", url="https://docs.reya.network"))
    markup.add(InlineKeyboardButton("⚡ Staked Platform", url="https://app.reya.network"))
    markup.add(InlineKeyboardButton("📊 Trading Platform", url="https://app.reya.xyz"))
    markup.add(InlineKeyboardButton("❓ FAQ", url="https://0xobhan.notion.site/Reya-Network-FAQ-222c0c1c90684efdbdc5af9038bd8f5d?pvs=4"))

    bot.send_message(message.chat.id, "🔗 **Reya Information**", reply_markup=markup, parse_mode="Markdown")


# Start bot
bot.polling()