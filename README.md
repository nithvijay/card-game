# Websockets Card Game

The goal of this project is to build a multiplayer card game using Socket.io.

## Running the code

```console
$ docker-compose up # to run the website
$ docker-compose up --build # if there are changes to the Dockerfile or requirements.txt
$ docker-compose down # to close the website fully and delete database
```

Then, go to `localhost:3000` to see the website

> The container environment still needs work. The anonymous volumes used do not get deleted, so `docker volume prune` needs to be done every once in a while.

## Things to do:
- [x] Create Container environment
- [x] Make basic websocket in Flask
- [x] Connect the database
- [x] Produce chat application with React
- [x] Make basic card game with React
- [x] Containerize React app
- [x] Refine/refactor basic card game
- [x] Host basic card game with React frontend, Flask backend, and Redis database
- [ ] Make fully featured card game (Vue?)
- [ ] Deploy fully featured card game


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


## Game Notes
- Stage 1 - discard
  - All except Sheriff have option to Discard
- Stage 2 - select cards
  - All except Sheriff need to select cards
- Stage 3 - inspection
  - Sheriff chooses to inspect certain cards
- Stage 4 - reveal and declare points