FROM python:3.11-alpine

WORKDIR /code

COPY requirements.txt /code
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt && \
    python3 -m pip install -U discord.py

COPY src/openai_discord_bot.py /code/src

CMD ["python3", "/code/src/openai_discord_bot.py"]
