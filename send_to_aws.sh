#! /bin/sh

scp -r $(PWD)/{requirements.txt,Dockerfile,docker-compose.yml,.env,check_permissions.sh} discord-api:~/discord-bot
scp -r $(PWD)/{src/openai_discord_bot.py,src/openai_logger.py} discord-api:~/discord-bot/src
