import os
import datetime as dt
import time

from dotenv import load_dotenv
import discord
import openai

from openai_logger import LogDataManager

load_dotenv()

discord_token = os.environ.get('AUTH_TOKEN')

# connect to discord client
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

# Set up the OpenAI API client
openai.api_key = os.environ.get('OPENAI_API_KEY')
# Set up the model and prompt
model_engine = os.environ.get('MODEL_ENGINE')

log_db_path = os.environ.get('LOGS_SQLITE_DB')
log_db = LogDataManager(f'sqlite:///{log_db_path}')


error_channel_id = os.environ.get('ERROR_CHANNEL_ID')


@client.event
async def on_ready():
    print(f'We have logged in as {client}')


def chunked_messages(content: str, chunk_size: int = 2000) -> list[str]:
    """Given a string, chunk it into a list of strings with the size of chunk_size
    characters.
    No empty chunks are given.

    Args:
        content    (str): String to split up into chunks. If an empty string is given, 
        chunk_size (int): Number of characters to have in each chunk.

    Returns:
        list[str]: List of strings which are of size maximum chunk_size
    """
    if len(content) == 0:
        return ['']
    chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]
    return [chunk for chunk in chunks if chunk]


async def send_message(channel, content: str, retries=5):
    """Sends a message to the specified channel.

    Args:
        channel (discord.Channel): The channel to send the message to.
        content (str): The content of the message to send.
        retries (int, optional): The number of retries to attempt. Defaults to 5.
    """
    while retries >= 0:
        try:
            if len(content) == 0:
                await channel.send('Empty message')
            for message in chunked_messages(content):
                await channel.send(message)
            return
        except discord.errors.HTTPException:
            print("Error sending message. Retrying in 5 milliseconds...")
            time.sleep(0.005)
            retries -= 1
        except Exception:
            raise
    await send_error_message(f'error sending message of size {len(content)}')


async def send_error_message(content: str):
    """Sends an error message to the error channel.

    Args:
        content (str): The content of the message to send.
    """
    try:
        error_channel = discord.utils.get(client.get_all_channels(), name=error_channel_name)
        await error_channel.send(content)
    except Exception as e:
        # send the message instead on the first channel we can
        random_channel = discord.utils.get(client.guilds).text_channels[0]
        await send_message(random_channel, f'Couldnt find error channel. Got error {type(e).__name__}')
        raise


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    try:
        # Generate a response
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=message.content,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
    except openai.error.RateLimitError:  # should do something special when this happens, such as retry
        await send_error_message(error_channel_id, message, 'Got RateLimitError from openai api')
        raise
    except Exception:
        raise

    response = completion.choices[0].text

    log_db.log_data(prompt=message.content,
                    response=response,
                    time=dt.datetime.fromtimestamp(int(completion.created)),
                    tokens=completion.usage['total_tokens'],
                    completion_obj=completion)

    await send_message(message.channel, response)

client.run(discord_token)
