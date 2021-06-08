# Websockets Card Game

The goal of this project is to build a multiplayer card game using websockets.

## Running the code

```console
$ docker-compose up # to run the website
$ docker-compose up --build # if there are changes to the Dockerfile or requirements.txt
$ docker-compose down # to close the website fully
```


Alternatively, build the environment manually
```console
$ docker build -t cardgame .
$ docker run -it --rm --name cg \
    --mount type=bind,source="$(pwd)",target=/code \
    -p 5000:5000 \
    cardgame
$ docker exec -it cg bash 
```

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


# Notes

## **Redis Notes**
```console
$ docker exec -it redis bash
$ redis-cli
```

Database Notes:

Name | Description | Data Type | Redis Command
---|---|---|---
`card_index` | Index for cards | Set | `SMEMBERS`
`set_of_rooms` | Index for rooms | Set | `SMEMBERS`
`room_data:<ASDF>` | 
`room_members:<ASDF>` | SIDs of users in the room | Set | `SMEMBERS`
`card:<Sword>` | Attributes for card | Many Fields | `HGET`/`HGETALL`
`<nXM8LkLfjGYCs0dlAAAJ>` | Name of given sid | Single Field | `GET` 


### What `room_data` contains

```python
room_data = {
    userCards=[[<Card Object>], [...], ...]
    centerCards=[<Card Object>, ...]
    userNames=[], # ordered
    userSIDs=[], 
    scores={},
    turn=...
}
```