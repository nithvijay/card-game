# Websockets Card Game

The goal of this project is to build a multiplayer card game using Socket.io.

## Running the code

```console
$ docker-compose up # to run the website
$ docker-compose up --build # if there are changes to the Dockerfile or requirements.txt
$ docker-compose down # to close the website fully
```

Then, go to `localhost:3000` to see the website

> The container environment still needs work. The anonymous volumes used do not get deleted, so `docker system purge --volumes` needs to be done every once in a while.

## Things to do:
- [x] Create Container environment
- [x] Make basic websocket in Flask
- [x] Connect the database
- [x] Produce chat application with React
- [x] Make basic card game with React
- [x] Containerize React app
- [ ] Refine/refactor basic card game
- [ ] Host basic card game with React frontend, Flask backend, and Redis database
- [ ] Make fully featured card game
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

### React
- React Docs - https://reactjs.org/docs/getting-started.html
- React Crash Course - https://www.youtube.com/watch?v=w7ejDZ8SWv8
- Using the socket-io client - https://dev.to/bravemaster619/how-to-use-socket-io-client-correctly-in-react-app-o65

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
`room_data:<ASDF>` | All game data | Single Field | `GET`
`room_members:<ASDF>` | SIDs of users in the room | Set | `SMEMBERS`
`card:<Sword>` | Attributes for card | Many Fields | `HGET`/`HGETALL`
`<nXM8LkLfjGYCs0dlAAAJ>` | Name of given sid | Single Field | `GET` 


### What `room_data` contains

```python
room_data = {
    userCards=[[<Card Object>], [...], ...] 
    centerCards=[<Card Object>, ...] # unordered/based on centerCardsPlayerIndex
    userNames=[],
    userSIDs=[], 
    scores={},
    turn=..., # unused
    playedThisTurn: [],
    centerCardsPlayerIndex: []
}
```

The keys which have lists as values (besides `centerCards`) are ordered, meaning that each index corresponds to a single player.