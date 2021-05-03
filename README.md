# chat-app

1. To run this app you'll need to have docker-compose installed.
    Here are some instructions on how to set that up on MacOS: https://docs.docker.com/docker-for-mac/install/

    Double check that docker got installed by running `docker-compose --version`.

2. Build the container by running the following from the repository's root folder: `docker-compose -f docker/chat-app.yml build`

2. Then start the docker container containing the app: `docker-compose -f docker/chat-app.yml up`

3. You should now be able to access the app at `http://0.0.0.0:8000/chat`


The app navigation build up:

```

                 -> Messages (search, view, create new) -> Thoughts (view, create new)
                |
Conversations ---
(search, view)  |
                 -> Create new conversation
```


---------------

To run the tests (requires the docker container to be built beforehand):
`docker-compose -f docker/chat-app.yml run chat-app python manage.py test chat.tests`
