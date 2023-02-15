# Python OpenAI Discord Bot
I created this simple Python program to allow me to more easily interact with the powerful OpenAI API, within a Discord server. Once you've setup a discord bot and an have obtained an OpenAI API key, this is incredibly easy to do. 

## Features
- Direct communication with OpenAI text model within discord server
- Logging of all communications and tokens used in SQLite database

## How it Works
Below is a very simple example of how this can be achieved. For the full example, see `docs/simple_test_client.py`:
```python
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
```

# Setup Instructions
## Basic Steps
1. Setup a discord bot and invite it to your server
2. Setup an OpenAI account and obtain an API key
3. Add the required variables in a file called `.env`. Use `.env.example` as a template.
4. Run with or without docker (see "Running on AWS with Docker and Docker Compose" and "Running without Docker")

## Running on AWS with Docker and Docker Compose
1. Create new AWS EC2 instance, connect to it using SSH, etc
2. Install docker and docker compose
3. Clone the project into a `discord-bot` folder
4. Create a `data` folder in the `discort-bot` folder
5. Give full write permissions for this directory. Otherwise the container cannot use its database in this folder:
    `sudo chmod a+w data`

6. Start the containers: `docker compose up --build -d`

## Running without Docker
I haven't tested this, but it should work. Note that this will be less secure.
1. Ensure Python and PIP are installed.
2. Install requirements: `python3 -m pip install -r requirements.txt`
3. Run the discord server: `python3 src/openai_discord_bot.py`

# Examples
## Asking for markdown-style report aboutsome topic
write me a 5000 word report about **Insert Topic Here**. Use markdown-style formatting with headings for major sections and sub-sections. Include at least 5 major sections and at least 3 sub-sections within each major section. There should be an abstract section, an introduction section, and a conclusion section as well.

## Planed Future Features
- [ ] Log number of tokens used in message and response separately
- [ ] Allow for usage of slash `/` commands from within discord server e.g. `/ask what is the linux kernel?`
- [ ] Allow for OpenAI image model (and possibly other models) to be used as well e.g. `/createimage panda riding bicyle`
- [ ] Better error handling. For example, if the OpenAI API sends an error response, the script is unable to respond properly. It should
send an error message to the `ERROR_CHANNEL_NAME` channel (as defined in `.env`), but instead it causes the code to output an error
(possibly due to synchronous code running slowly within async block?).
