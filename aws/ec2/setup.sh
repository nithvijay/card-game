#!/usr/bin/bash

sudo amazon-linux-extras install -y nginx1 redis6 python3.8
sudo yum -y update
sudo yum install -y ruby wget emacs

sudo mkdir /data
sudo chmod -R 775 /data 

wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
. ~/.nvm/nvm.sh
nvm install node --lts

sudo nginx

