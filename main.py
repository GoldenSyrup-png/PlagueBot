import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import time
import asyncio
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

load_dotenv()

TOKEN = os.getenv("API_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Define the scope and authenticate
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open the spreadsheet by URL
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1fwgiFHMTBZko9G7ps6bLCeuM51v78vRnhk-BogeXJno/edit?usp=sharing"
sheet = client.open_by_url(SPREADSHEET_URL)
worksheet = sheet.sheet1

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f'Message from {message.author}: {message.content}')
    await bot.process_commands(message)


@bot.tree.command(name="botonline", description="Is the bot online?")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"As of {datetime.today().strftime('%Y-%m-%d %H:%M:%S')} I am working")

@bot.tree.command(name="purge", description="Delete the last 50 messages.")
async def purge(interaction: discord.Interaction):
    if interaction.user.name == "goldensyrup0":
        channel = interaction.channel
        await channel.purge(limit=50)
        await interaction.response.send_message("Deleted the last 50 messages.")
    else:
        await interaction.response.send_message("Fail")

@bot.tree.command(name="request", description="Make a request that i can add to the bot :)")
async def request(interaction: discord.Interaction, message: str):
    user_id = 769597229723680802
    user = interaction.user
    member = user.name
    nickname = user.nick

    Data = {
        "Message": [message],
        "User":[member],
        "Nickname":[nickname],
        "Time":[datetime.today().strftime('%Y-%m-%d %H:%M:%S')]
    }
    Data = pd.DataFrame(Data)
    
    records = worksheet.get_all_records()
    OldData = pd.DataFrame(records)

    NewData = pd.concat([OldData,Data], ignore_index=True)

    worksheet.clear()
    worksheet.update([NewData.columns.values.tolist()] + NewData.values.tolist())

    user = await bot.fetch_user(user_id)
    await user.send(f"{Data}")
    await interaction.response.send_message("Thank you for your request, ill (Hopefully) get around to it")

@bot.tree.command(name="get_my_id", description="Get your Discord User ID")
async def get_my_id(interaction: discord.Interaction):
    user_id = interaction.user.id  # Get the ID of the user who invoked the command
    await interaction.response.send_message(f"{user_id}")

@bot.tree.command(name="bye", description="Bye Bye")
async def get_my_id(interaction: discord.Interaction):
    await interaction.response.send_message("https://tenor.com/view/bye-gif-10524392059479647")

bot.run(TOKEN)
