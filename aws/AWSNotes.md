# AWS Notes

## Resource Set-up

### EC2
- SSL
  - Install snapd
    - https://forum.snapcraft.io/t/unofficial-snapd-repository-for-amazon-linux-2/24269/7
    - https://snapcraft.io/docs/installing-snap-on-red-hat
  - Install certbot - https://certbot.eff.org/lets-encrypt/centosrhel8-nginx

### Code Pipeline
- EC2
  - Create instance role for EC2
    - AmazonEC2RoleforAWSCodeDeploy
  - Add tag to reference in CodeDeploy
  - CodeDeploy Agent
    - https://docs.aws.amazon.com/codedeploy/latest/userguide/codedeploy-agent-operations-install-linux.html
- CodeDeploy
  - `appspec.yml` is needed
  - Service Role
    - AWSCodeDeployRole
  - Deployment Group
    - Use service role created earlier
    - In Environment config, select EC2
  - logs are `/var/log/aws/codedeploy-agent`
- CodePipeline
  - It creates its own service role
  - Need to connect GitHub and authorize AWS to a particular repo

### ECR
- First time set-up
```console
$ aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <Account ID>.dkr.ecr.us-east-1.amazonaws.com
```

- Push commands
```console
$ docker build -t card-game-server .
$ docker tag card-game-server:latest <Account ID>.dkr.ecr.us-east-1.amazonaws.com/card-game-server:latest
$ docker push <Account ID>.dkr.ecr.us-east-1.amazonaws.com/card-game-server:latest
```

### S3
```
$ cd client
$ npm run build
$ aws s3 ls
$ aws s3 sync dist s3://card-game-client --delete
```
https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteAccessPermissionsReqd.html
https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-commands.html