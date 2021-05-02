# chat-app

> The instructions are assuming a mac OS environment.

1. Install docker following instructions here: https://docs.docker.com/docker-for-mac/install/
2. From the repository's root folder run the docker container: `docker-compose -f docker/chat-app.yml up`


In development from root folder run:
`docker-compose -f docker/chat-app.yml build`
`docker-compose -f docker/chat-app.yml run chat-app bash`
