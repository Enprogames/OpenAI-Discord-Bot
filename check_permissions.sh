#!/bin/sh

sqlite_db_dir="/data/${LOGS_SQLITE_DB}"

# check to see if the file exists. if not, try to create it
if [ ! -f $sqlite_db_dir ]; then
    echo "DB file not found at ${sqlite_db_dir}. Attempting to create..."
    echo "" > $sqlite_db_dir
    # check to see if the file was created
    if [ ! -f $sqlite_db_dir ]; then
        echo "DB file could not be created. Exiting."
        exit 1
    else
        echo "Success."
    fi
fi

# Check the permissions of the database file
if [ ! -w $sqlite_db_dir ]; then
  echo "The SQLite database file is read only. Trying to give write permissions..."
  chmod u+w $sqlite_db_dir
fi
if [ ! -w $sqlite_db_dir ]; then
  echo "The SQLite database file is read only. Exiting."
  exit 1
fi

# Start the API service
python3 /code/openai_discord_bot.py
