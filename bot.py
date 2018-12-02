# Work with Python 3.6
import discord
import requests
import json
import nltk
from gymFinder import findGym
from datetime import datetime


confidence_threshold = 0.14

current_raids = []

TOKEN = '[DISCORD_TOKEN]' # Add your discord token here.

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    if message.content.startswith('!print'):
        if len(current_raids) == 0:
            response = f"No Raids yet, you should add one."
        else:
            response = f"current_raids: \n"
            for raid in current_raids:
                response+=f"{raid}\n"
        await client.send_message(message.channel, response)
    else:

        sentence = message.content

        gym, confidence = findGym(sentence)

        if not ((gym == None) or (confidence == None)):

            if confidence > confidence_threshold:
                response = f"Looks like you're looking for {gym} with {(confidence*100):.3f}% confidence :)"
                current_raids.append(f"{gym} added @ {datetime.now().strftime('%a, %I:%M%p')} by {message.author}")
                await client.send_message(message.channel, response)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)