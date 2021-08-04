#!/usr/bin/bash

sudo nginx -s reload
sudo systemctl daemon-reload
sudo systemctl restart flask-server

