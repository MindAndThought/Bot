# import client_details as c
import discord, logging, json

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

tFile = open("config.json", "r")  # opens file
config = tFile.read()  # reads the entire file at once
tFile.close()  # closes the file
config = json.loads(config)

# print(config["prefix"])
client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if (message.author == client.user) or not (
        message.content.endswith(config["postfix"])
    ):
        return
    else:
        # if message.content.startswith("$hello"):
        #     await message.channel.send("Hello!")
        print(message.content)


client.run(config["token"])