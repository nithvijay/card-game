#!/usr/bin/bash

echo "Reloading Nginx..."
sudo nginx -s reload
echo "Restarting Flask..."
sudo systemctl daemon-reload
sudo systemctl restart flask-server

