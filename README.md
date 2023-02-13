
## Asking for markdown-style report
write me a 5000 word report about **Insert Topic Here**. Use markdown-style formatting with headings for major sections and sub-sections. Include at least 5 major sections and at least 3 sub-sections within each major section. There should be an abstract section, an introduction section, and a conclusion section as well.

## Running without docker-compose
To run a Docker container without using docker-compose, you can use the following commands:

1. Build:

    `docker build

1. Spin up and run the container in detached mode:

    `docker run -d <image_name>`
    
    With database volume:

    `docker run -d --name discord_ai_bot -v ./openai_data_log.sqlite3:/data/openai_data_log.sqlite3 discord_ai_bot`
    

2. Stop the container:

    `docker stop <container_id>`

3. Delete the container and its contents:

    `docker rm <container_id>`

4. View the logs of the container:

    `docker logs <container_id>`


Note: You may need to use the -f flag to follow the logs and the --tail flag to limit the number of log lines displayed.

## Running on AWS
1. Install docker and docker compose
2. Clone the project into a `discord-bot` folder
3. Create a `data` folder in the `discort-bot` folder
4. Give full write permissions for this directory. Otherwise the container cannot use its database in this folder:
    `sudo chmod a+w data`

5. Start the containers: `docker compose up --build -d`
