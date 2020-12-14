# Docker Commands

```console
$ docker build -t cardgame:1.0 .
$ docker run -it --rm --name cg \
    --mount type=bind,source="$(pwd)",target=/code \
    -p 5000:5000 \
    cardgame:1.0
$ docker exec -it cg bash 
```

Goal: Multiplayer Card-Based Game

1. Server Side Requests (AJAX) via HTTP
2. Websockets
    1. Flask - Flask-SocketIO
    2. Django - Django-Channels
    3. Express.js + Vue 

Things to do:
1. Make websocket in Flask
2. Connecting the database
3. Connect frontend and backend

