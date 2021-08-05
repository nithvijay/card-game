#!/usr/bin/bash
export REACT_APP_AWS_ADDRESS=https://inspectorgame.com

cd /home/ec2-user
sudo mv aws/ec2/nginx.conf /etc/nginx/nginx.conf
sudo mv aws/ec2/flask-server.service /etc/systemd/system/flask-server.service
sudo chown -R ec2-user .

cd client
. /home/ec2-user/.nvm/nvm.sh
# install sometimes fails because lack of memory, so multiple attempts are needed
# TODO: Find better solution
npm install
npm install
npm install
npm run build 
sudo rm -rf /data/dist
sudo mv dist/ /data/

cd ../server
python3.8 -m venv card-game-env
source card-game-env/bin/activate
pip install -r requirements.txt


