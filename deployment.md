use reverse proxy, why wsgi server great at executing python code, but not good at serving static files

1. Create an account on aws
2. Login in aws console
3. search iAM service and validate the users if you wanna add users to your account
4. generate a ssh key 4096
5. EC2 service > key pairs > import key pair > upload your key pair
6. EC2 service > instances > launch instance
7. name your instance and set the number of instances in 1, select amazon linux
8. t2.micro is free tier, select it
9. key pair login > select your key pair
10. Select allow ssh traffic from anywhere
11. Allow http traffic from the internet
12. Configure the store 1x30 GIB gp2 Root volume
13. Create an instance
14. EC2 instances > select your instance > connect > copy the ssh command> copy the public ipv4
15. Open your terminal and paste the ssh command "ssh-add /path/to/your/private/key" enter the password
16. ssh ec2-user@your-public-ipv4
17. this should connect to the server

github deploy
1. inside the server ec2 generate a new key ssh-keygen -t ed25519 -b 4096
2. enter the password
3. copy the public key cat /home/ec2-user/.ssh/id_ed25519.pub
4. go to github > settings > deploy keys > add deploy key > paste the public key

install docker and git
1. insider the server ec2
2. sudo yum update -y
3. sudo yum install git -y
4. sudo amazon-linux-extras install docker -y
5. sudo systemctl enable docker.service
6. sudo systemctl start docker.service
7. sudo usermod -aG docker ec2-user
8. exit
9. ssh ec2-user@your-public-ipv4
10. sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

11. git clone your repo
12. cd your-repo
13. git pull origin
14. cp .env.example .env
15. nano .env
16. change the environment variables
17. copy the hostname and instance public ipv4 dns and put in allowed hosts env variable
18. paste the next command docker-compose -f docker-compose-deploy.yml up -d
19. docker-compose -f docker-compose-deploy.yml run --rm app -sh -c "python manage.py createsuperuser"
20. its all

Update the server
1. commit your changes in github
2. ssh ec2-user@your-public-ipv4
3. cd your-repo
4. git pull origin
5. docker-compose -f docker-compose-deploy.yml build app
6. docker-compose -f docker-compose-deploy.yml up --no-deps -d app

