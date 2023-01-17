FROM python:3.10.8-slim

ENV token=token

RUN useradd --create-home --no-log-init --shell /bin/bash skynet

WORKDIR /home/skynet

RUN mkdir sbot

COPY --chown=skynet:skynet skynet_bot sbot/

WORKDIR /home/skynet/sbot

RUN chmod +x skynet_bot.py

RUN pip3 install --no-cache-dir -r requirements.txt

USER skynet

CMD python3 skynet_bot.py -t ${token}