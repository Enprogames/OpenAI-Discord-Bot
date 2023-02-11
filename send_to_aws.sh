#! /bin/sh

scp -r $(PWD)/{requirements.txt,Dockerfile,docker-compose.yml,.env,src/openai_discord_bot.py,src/openai_logger.py} discord-api:~/discord-bot
