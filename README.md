# chat-app

## Setup

1. Pull the repo via git: `git clone https://github.com/BetyMehide/chat-app.git`

2. To run this app you'll need to have docker-compose installed.
    Here are some instructions on how to set that up on MacOS: https://docs.docker.com/docker-for-mac/install/

    Double check that docker got installed by running `docker-compose --version`.
3. Add `SECRET_KEY = "test"` to `src/config/settings.py`

4. Build the container by running the following from the repository's root folder: `docker-compose -f docker/chat-app.yml build`

5. Then start the docker container containing the app: `docker-compose -f docker/chat-app.yml up`

6. You should now be able to access the app at `http://0.0.0.0:8000/chat`


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
