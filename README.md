# Demo MySQL Test Database

## .gitpod.yml

We can get the most recent snapshot with:

```bash
KEY=`aws s3 ls  s3://devgraph-devspaces-demos/dockerdb/edb1/mysql-data/ | awk '{print $4}' | sort | tail -n 1`
aws s3 cp s3://devgraph-devspaces-demos/dockerdb/edb1/mysql-data/$KEY edb1/mysql-data/
```

To fix to a particular snapshot, set:
```bash
KEY=`2022-07-01_061024_mysql-data.tar.gz`
aws s3 cp s3://devgraph-devspaces-demos/dockerdb/edb1/mysql-data/$KEY edb1/mysql-data/
```

## Snapshots

Last known good snapshot: `edb1/mysql-data/2022-07-01_061024_mysql-data.tar.gz`

# Docker 

## Dumping MySQL to File

```sh
docker exec mysql-server /usr/bin/mysqldump -u root --password=mypass employees | gzip -9 -c > `date +"%Y-%m-%d_%H%M%S"`__backup.sql.gz
```

## Restoring MySQL Dump from File

From a fresh instantiation of the MySQL database, we can do:

```sh
docker exec mysql-server mysql -u root --password=mypass -e "CREATE DATABASE employees"
gunzip -c edb1/mysql-data/2022-07-03_204450__backup.sql.gz | docker exec -i mysql-server mysql -u root --password=mypass employees
```

## Clean shutdown

```sh
docker exec mysql-server /usr/bin/mysqladmin -uroot -pmypass shutdown
```