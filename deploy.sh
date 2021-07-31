# # first time

# sudo amazon-linux-extras install -y nginx1
# sudo yum update
# sudo yum install -y emacs git

# sudo mkdir /data
# sudo chmod -R 775 /data 


# curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
# . ~/.nvm/nvm.sh
# nvm install node

# git clone https://github.com/nithvijay/card-game.git
# sudo mv card-game/nginx.conf /etc/nginx/nginx.conf
# cd card-game/client
# npm install
# npm run build
# rm -r /data/build
# mv build/ /data/
# sudo nginx

# cd ../server
# python3 -m venv card-game-env
# source card-game-env/bin/activate


# otherwise
sudo mv nginx.conf /etc/nginx/nginx.conf

export ENVIRONMENT=PROD
export AWS_ADDRESS=http://ec2-100-25-192-54.compute-1.amazonaws.com
export REDIS_ADDRESS=redis-one.uzmwbi.0001.use1.cache.amazonaws.com
export REACT_APP_AWS_ADDRESS=$AWS_ADDRESS

cd client
npm install
npm run build
rm -r /data/dist
mv dist/ /data/
sudo nginx -s reload

cd ../server
pkill -u ec2-user python3
source card-game-env/bin/activate
pip install -r requirements.txt
nohup python3 main.py &