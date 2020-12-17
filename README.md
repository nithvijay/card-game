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

Things to do:
- [x] Create Container environment
- [x] Make basic websocket in Flask
- [ ] Connect the database
- [ ] Make basic card game
- [ ] Do Vue.js sample project
- [ ] Link Flask backend and Vue.js frontend
- [ ] Make fully featured card game
- [ ] Deploy to GCP or Heroku

Tutorials:
1. Websockets in Flask - https://flask-socketio.readthedocs.io/en/latest/
2. Docker Part 1 - https://docs.docker.com/get-started/
3. Docker Part 2 - https://docs.docker.com/get-started/part2/
4. Docker-Compose - https://docs.docker.com/compose/gettingstarted/
