#! /bin/sh

scp -r $(PWD)/{requirements.txt,Dockerfile,docker-compose.yml,.env,src/openai_discord_bot.py,src/openai_logger.py,check_permissions.sh} discord-api:~/discord-bot
