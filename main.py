import discord  # to connect to discord and crap
from discord.ext import commands
import logging  # for simple logging
import json  # to read the config.json file
import requests

# from pathlib import Path  # for paths (not using OS, but could)

# read json file and get bot details
bot_details = open("config.json", "r")
# creates a dict from the json it just read
config = json.loads(bot_details.read())
bot_details.close()

# create the bot
bot = commands.Bot(command_prefix=config["prefix"], case_insensitive=True)
bot.config_token = config["token"]
logging.basicConfig(level=logging.INFO)


@bot.event
async def on_ready():  # when connected and ready to go
    print(f"----- Logged in as {bot.user.name} : {bot.user.id} -----")
    # change bot activity
    await bot.change_presence(activity=discord.Game(name="Chat with me, please :)"))


@bot.command(name="hi", aliases=["hello"])
# by default, the below will be triggered by !_hi, but since we made the name "hi" and give aliases as "hello"
# the below will only be triggered by !hi and !hello
async def _hi(ctx):  # _hi so you don't overwrite an existing function
    await ctx.send(f"Hi, {ctx.author.mention}!")


@bot.command()
# the below code will be triggred when someone says !echo
# without the * the message will be a tuple and not a string
async def echo(ctx, *, message=None):  # !echo
    message = message or "Please provide a message to copy"
    await ctx.message.delete()  # deletes users original message
    await ctx.send(f"{message}!")  # sends the message in their place


weather_api_url = "http://api.openweathermap.org/data/2.5/weather?"


@bot.command(name="weather")
async def _weather(ctx, *, message=None):
    message = message or "Look out the windows"
    complete_url = (
        weather_api_url + "appid=" + config["weather_api_key"] + "&q=" + message
    )
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        print(x, y)
        celsius = round(y["temp"] - 273.15)
        # (0°C × 9/5) + 32
        fahrenheit = round(celsius * 9 / 5) + 32
        formatted_resonse = f"Weather: {x['weather'][0]['description']}\n"
        formatted_resonse += (
            f"Temperature: {celsius}{chr(176)}C ({fahrenheit}{chr(176)}F)\n"
        )

        celsius = round(y["temp_max"] - 273.15)
        fahrenheit = round(celsius * 9 / 5) + 32
        formatted_resonse += (
            f"Max Temperature: {celsius}{chr(176)}C ({fahrenheit}{chr(176)}F)\n"
        )

        celsius = round(y["temp_min"] - 273.15)
        fahrenheit = round(celsius * 9 / 5) + 32
        formatted_resonse += (
            f"Min Temperature: {celsius}{chr(176)}C ({fahrenheit}{chr(176)}F)\n"
        )

        await ctx.send(
            # f"{celsius}{chr(176)}C ({fahrenheit}{chr(176)}F)"
            formatted_resonse
        )  # sends the message in their place
    else:
        print(x)
        await ctx.send(f"Could not get data!")


bot.run(bot.config_token)