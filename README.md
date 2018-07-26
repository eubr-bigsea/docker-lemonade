Docker Lemonade
===============

Project for running Lemonade's projects all together

Clone and go into directory
```
git clone git@github.com:eubr-bigsea/docker-lemonade.git
cd docker-lemonade

```

Running docker hub available containers
-------
```
docker-compose pull
docker-compose up -d --no-build
```
Wait all services to go up and access http://localhost:23450


Building containers from projects
---------------
```
git submodule init
git submodule update --remote
docker-compose up -d mysql redis
# wait a little bit
docker-compose up -d --build
```

Using swarm
-----------
```
docker stack deploy -c docker-stack.yml lemonade

```

Troubleshooting
---------------
### UnixHTTPConnectionPool ... Read timed out
Set the following environment variables and run compose up again
```
export DOCKER_CLIENT_TIMEOUT=120
export COMPOSE_HTTP_TIMEOUT=120
```
