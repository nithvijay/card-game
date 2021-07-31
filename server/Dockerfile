FROM python:3.8-slim-buster

RUN python3 -m pip install --upgrade pip

RUN useradd --create-home --shell /bin/bash worker
USER worker

WORKDIR /home/worker

ENV REDIS_ADDRESS=redis

COPY --chown=worker:worker requirements.txt requirements.txt
RUN python3 -m pip install --user -r requirements.txt

COPY --chown=worker:worker . .

EXPOSE 5000

CMD ["python", "main.py"]
