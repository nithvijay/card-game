# Websockets Card Game

The goal of this project is to build a multiplayer card game using websockets.

## Running the code

```console
$ docker-compose up # to run the website
$ docker-compose up --build # if there are changes to the Dockerfile or requirements.txt
$ docker-compose down # to close the website fully and delete database
```


Alternatively, build the environment manually
```console
$ docker build -t cardgame .
$ docker run -it --rm --name cg \
    --mount type=bind,source="$(pwd)",target=/code \
    -p 5000:5000 \
    cardgame
$ docker exec -it cg bash # for debugging
```

Then, go to `localhost:5000` to see the website.

Things to do:
- [x] Create Container environment
- [x] Make basic websocket in Flask
- [x] Connect the database
- [x] Produce chat application for game
- [ ] Make basic card game
- [ ] Do Vue.js sample project
- [ ] Link Flask backend and Vue.js frontend
- [ ] Make fully featured card game
- [ ] Deploy to GCP or Heroku

## Tutorials
### Websockets
- `Flask-SocketIO` - https://flask-socketio.readthedocs.io/en/latest/
- Socket.IO Javascript Client API Docs - https://socket.io/docs/v3/client-api/index.html

### Docker
- Docker Part 1 - https://docs.docker.com/get-started/
- Docker Part 2 - https://docs.docker.com/get-started/part2/
- Docker-Compose - https://docs.docker.com/compose/gettingstarted/
- Dockerfile Reference - https://docs.docker.com/engine/reference/builder/

### Redis
- Redis DB and CLI - https://www.tutorialspoint.com/redis/redis_environment.htm
- Python Redis API - https://github.com/andymccurdy/redis-py
- Redis Docker Image - https://hub.docker.com/_/redis



**Redis Notes**
```console
$ docker exec -it redis bash
$ redis-cli
```

