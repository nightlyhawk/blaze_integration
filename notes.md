$ docker-compose -f docker-compose.prod.yml down -v
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
$ docker stop $(docker -p -q)
$ docker rm $(docker -p -a -q)
$ docker logs "container_name"
$ scp -i /path/to/your-key.pem -r /path/to/local/directory username@ec2-instance-public-ip:/path/to/remote/directory
