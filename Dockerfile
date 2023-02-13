# Use the Python 3.11 Alpine image
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /code

# create user with reduced permissions
RUN adduser -D appuser

# create the data directory and give ownership to user. this will allow the volume in docker-compose.yml
# to be accessible to this user.
RUN mkdir /data
RUN chown appuser:appuser /data

# Create a user with reduced permissions
USER appuser

# Run the pip install command in user mode to install the dependencies
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --user -r /code/requirements.txt

# Copy the application code from the host machine to the container
COPY ./src/ /code/
COPY ./check_permissions.sh /code/

# Set the entry point for the container to run the python application
ENTRYPOINT ["./check_permissions.sh"]
