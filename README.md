# Docker Commands

```console
$ docker build -t cardgame:1.0 .
$ docker run -it --rm --name cg \
    --mount type=bind,source="$(pwd)",target=/code \
    -p 5000:5000 \
    cardgame:1.0
$ docker exec -it cg bash 
```
