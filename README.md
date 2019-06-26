Docker Lemonade
===============

Project for running Lemonade's projects all together

Clone and go into directory
```
git clone git@github.com:eubr-bigsea/docker-lemonade.git
cd docker-lemonade

```
Update project dependencies:
```
git submodule update --init --checkout
```

Running docker hub available containers
-------
```
docker-compose pull
docker-compose up -d --no-build
```
Wait all services to go up and access http://localhost:23456. To change the listening port, change the `docker-compose.yaml` file, replace the `ports` configuration under the `citrus` service configuration.


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
Clusters are configured in tables from `stand` service. A user interface is under progress. If you need to add a cluster configuration, you need to connect to the MySQL service and add a record in `cluster` table:

```
% sudo docker-compose exec mysql mysql -u root -plemon stand
mysql> INSERT INTO cluster(id, name, description, enabled, type, address, executor_cores, executor_memory, executors, general_parameters) VALUES (2, 'Spark cluster', 'Spark cluster', 1, 'MESOS', 'mesos://mesos-master:5050', 16, '2GB', 72, 'sparmesos.principal=lemonade,spark.mesos.secret=lemonade,spark.mesos.executor.home=/opt/spspark-2.3.0-bin-hadoop2.7');
```
The cluster type can be `MESOS`, `SPARK_LOCAL`, `SPARK` or `YARN`. The `address` must be a valid Spark master URL. The columns `executor_cores`, `executor_memory` and `executors` define the number of cores, memory and executors. These values are associated to the respective Spark parameters, as well parameters defined in `general_parameters`. They are well documented in Spark.


Using a HDFS Cluster
--------------------
A user interface is under progress. If you want to use a HDFS cluster, you need to connect to the MySQL service and add a record in `storage` table:

```
% sudo docker-compose exec mysql mysql -u root -plemon limonero
mysql> INSERT INTO storage(id, name, type, url, enabled) VALUES (2, 'HDFS cluster', 'HDFS', 'hdfs://hdfs-server:9000', 1);
```
The `url` column must be a valid HDFS URL and the cluster must be accessible from the containers.

Directories in the host machine
-------------------------------

By default, Lemonade will create 2 directories in the host machine, under the parent dir `/srv`:
- `/srv/lemonade/mysql-dev`, for the MySql database;
- `/srv/lemonade/storage` for HDFS local file system.

You can change these configurations in the `docker-compose.yaml` file.


DockerHub autobuild containers configuration
--------------------------------------------
* [Link GitHub and DockerHub](https://docs.docker.com/docker-hub/builds/link-source/)
* [Set up Automated builds](https://docs.docker.com/docker-hub/builds/)

Troubleshooting
---------------
### UnixHTTPConnectionPool ... Read timed out
Set the following environment variables and run compose up again
```
export DOCKER_CLIENT_TIMEOUT=120
export COMPOSE_HTTP_TIMEOUT=120
```

