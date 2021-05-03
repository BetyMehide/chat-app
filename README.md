# chat-app

1. To run this app you'll need to have docker installed.
    Here are some instructions on how to set up docker on MacOS: https://docs.docker.com/docker-for-mac/install/

    Double check that docker got installed by running `docker --version`.

2. From this repository's root folder start the docker container containing the app: `docker-compose -f docker/chat-app.yml up`

3. You should now be able to access the app at `http://0.0.0.0:8000/chat`


---------------

To run the test suit:
`docker-compose -f docker/chat-app.yml run chat-app python manage.py test chat.tests`
