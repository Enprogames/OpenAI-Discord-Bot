# Use the official Python 3.11 Alpine image as the base image
FROM python:3.11-alpine

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file to the container
COPY requirements.txt /code

# Upgrade pip and install the required packages
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt && \
    python3 -m pip install -U discord.py

# Copy the source code to the container
COPY ./src/openai_discord_bot.py /code
COPY ./src/openai_logger.py /code
COPY ./check_permissions.sh /code

# Create a non-root user named appuser
RUN addgroup -g 1000 appuser && \
    adduser -u 1000 -G appuser -s /bin/ash -D appuser

# Change the ownership of the /code directory to appuser
RUN chown -R appuser /code

# Use the appuser as the default user when running the container
USER appuser

# Start the bot when the container starts
CMD ["/code/check_permissions.sh"]
