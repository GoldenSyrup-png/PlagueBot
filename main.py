import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import time
import asyncio

load_dotenv()

TOKEN = os.getenv("API_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

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


@bot.tree.command(name="hellobot", description="Say hello to the bot!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.display_name}!")


@bot.tree.command(name="ping", description="Say ping to the bot!")
async def ping(interaction: discord.Interaction):
    message = "Yes, I'm working just fine -.-\nhttps://tenor.com/view/santa-go-to-hell-funny-gif-25523934"
    await interaction.response.send_message(message)

@bot.tree.command(name="hug", description="Give a hug to someone!")
async def ping(interaction: discord.Interaction, user: discord.User):
    og = interaction.user
    if og != user:
        await interaction.response.send_message(f"{og} gives a hug to {user}!")
    else:
        await interaction.response.send_message(f"You cant hug yourself {user} :'<")

@bot.tree.command(name="exploit", description="Give a hug to someone!")
async def ping(interaction: discord.Interaction, user_msg: str):
    message = f"As requested by {interaction.user}\n{user_msg}"
    await interaction.response.send_message(message)

@bot.tree.command(name="purge", description="Delete the last 50 messages.")
async def purge(interaction: discord.Interaction):
    if interaction.user == "goldensyrup0":
        channel = interaction.channel
        await channel.purge(limit=50)
        await interaction.response.send_message("Deleted the last 50 messages.", ephemeral=True)
    else:
        await interaction.response.send_message("Fail")

bot.run(TOKEN)
