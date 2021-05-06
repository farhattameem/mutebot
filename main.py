import os
import discord
import json

client = discord.Client()

my_secret = os.environ['token']

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  os.remove("users.json")

try:
    with open("users.json") as fp:
        users = json.load(fp)
except Exception:
    users = {}

def save_users():
      with open("users.json", "w+") as fp:
        json.dump(users, fp, sort_keys=True, indent=4)
      print(users)


def add_points(user: discord.User, points: int):
    id = str(user.id)
    if id not in users:
        users[id] = {}
    users[id]["points"] = users[id].get("points", 0) + points
    print("{} now has {} points".format(user.name, users[id]["points"]))
    save_users()

def get_points(user: discord.User):
    id = user.id
    if id in users:
        return users[id].get("points", 0)
    return 0

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print("{} used a message".format(message.author.name))
    if message.content.lower().startswith("!left"):
        msg = "You have {} messages left.".format(250 - int(get_points(message.author)))
        await message.channel.send(msg)
    add_points(message.author, 1)
client.run(my_secret)
