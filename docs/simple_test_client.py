import os

from dotenv import load_dotenv
import discord
import openai

load_dotenv()

discord_token = os.environ.get('AUTH_TOKEN')

# connect to discord client
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

# Set up the OpenAI API client
openai.api_key = os.environ.get('OPENAI_API_KEY')
# Set up the model and prompt
model_engine = 'text-davinci-003'


@client.event
async def on_ready():
    print(f'We have logged in as {client}')


@client.event
async def on_message(message):
    # Prevents the bot from responding to itself (and creating an infinite loop of self-responding messages)
    if message.author == client.user:
        return

    # Send a request to the OpenAI API for a response from the API, based on the received discord message
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=message.content,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # get the first generated response. since we specified n=1, there is only one anyways
    response = completion.choices[0].text

    # send the AI's response on the same channel as the message was sent
    await message.channel.send(response)

client.run(discord_token)
