# Demo MySQL Test Database

This repository shows how to:

1. Use Docker with MySQL as a test database
2. Populate MySQL with data stored and dynamically loaded from S3
3. Save MySQL data to S3 


## Snapshots

- Base database volume snapshot: `2022-07-18_181659_mysql-data.tar.gz`
- +20K entries volume snapshot: `2022-07-18_184803_mysql-data.tar.gz`
- +200K entries volume snapshot: `2022-07-18_201543_mysql-data.tar.gz`
- 10gb: `s3://devgraph-devspaces-demos/dockerdb/edb1/mysql-data/2022-07-06_231402`
- Uncompressed: 
- 1GB extra: `2022-07-19_200058`
- 6GB extra: `2022-07-19_202135`
# Docker 

## Clean shutdown

```sh
docker exec mysql-server /usr/bin/mysql -u root -pmypass -e 'flush tables;'
docker exec mysql-server /usr/bin/mysqladmin -uroot -pmypass shutdown
```

## MyDumper and MyLoader

Note, using the dump and load scripts are extremely slow.
```sh
mydumper -h 127.0.0.1 -u root  --password=mypass --database=employees --threads=8  --outputdir edb1/mysql-data/
```

```sh
myloader -h 127.0.0.1 -u root  --password=mypass --database=employees --threads=8 --directory edb1/mysql-data/2022-07-06_231402
```

## MySQL Fast write mode

Note, using volume mounts we do not need to do this.
```
docker run -d --name=mysql-server -p 3306:3306 \
        -e MYSQL_ROOT_PASSWORD=mypass       \
        -e MYSQL_DATABASE=testdb            \
        -v mysql-data:/var/lib/mysql        \
        mysql:5.7.38 --max-allowed-packet=67108864 \
        --innodb_buffer_pool_size=4G \
        --innodb_log_buffer_size=256M \
        --innodb_log_file_size=1G \
        --innodb_write_io_threads=16 \
        --innodb_flush_log_at_trx_commit=0 \
        --innodb-doublewrite=0
```


# Snapshots and S3

We can get the most recent snapshot with:

```bash
KEY=`aws s3 ls  s3://devgraph-devspaces-demos/dockerdb/edb1/mysql-data/ | awk '{print $4}' | sort | tail -n 1`
aws s3 cp --recursive s3://devgraph-devspaces-demos/dockerdb/edb1/mysql-data/$KEY edb1/mysql-data/$KEY
```

To fix to a particular snapshot, set:
```bash
KEY=`2022-07-01_061024_mysql-data.tar.gz`
aws s3 cp s3://devgraph-devspaces-demos/dockerdb/edb1/mysql-data/$KEY edb1/mysql-data/
```