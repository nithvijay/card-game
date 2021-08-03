#!/usr/bin/bash
export REACT_APP_AWS_ADDRESS=http://ec2-44-196-116-170.compute-1.amazonaws.com

sudo mv nginx.conf /etc/nginx/nginx.conf
sudo mv aws/ec2/flask-server.service /etc/systemd/system/flask-server.service

cd client
npm run build 
rm -r /data/dist
mv dist/ /data/

cd ../server
source card-game-env/bin/activate
pip install -r requirements.txt


