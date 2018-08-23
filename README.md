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
git submodule update --init --checkout
docker-compose up -d --build
```

Using swarm
-----------
```
docker stack deploy -c docker-stack.yml lemonade

```

Using remote spark cluster
--------------------------
Update the following lines in `config/juicer-config.yaml` with your own data
```
libprocess_advertise_ip: 127.0.0.1
spark.driver.host: your.hostname
```
To allow the connection it is needed to uncomment the lines bellow in
`docker-compose.yml` file
```
ports:
  - '37100-37399:37100-37399'
```
If you want to use spark envent log edit the following lines in
`config/juicer-config.yaml`
```
spark.eventLog.enabled: false
spark.eventLog.dir: hdfs://<namenode>:9000/path
spark.history.fs.logDirectory: hdfs://<namenode>:9000/path
```

Troubleshooting
---------------
### UnixHTTPConnectionPool ... Read timed out
Set the following environment variables and run compose up again
```
export DOCKER_CLIENT_TIMEOUT=120
export COMPOSE_HTTP_TIMEOUT=120
```
