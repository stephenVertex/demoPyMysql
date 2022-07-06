#1/bin/bash

#echo "Stopping Docker mysql-server cleanly..."
#docker exec mysql-server /usr/bin/mysqladmin -uroot -pmypass shutdown
#echo "...DONE"

echo "Archiving Database..."
#./docker-backup-volume/backup-volume.sh -v mysql-data -p edb1
#docker exec mysql-server /usr/bin/mysqldump -u root --password=mypass employees | gzip -9 -c > `date +"%Y-%m-%d_%H%M%S"`__backup.sql.gz
dname=`date +"%Y-%m-%d_%H%M%S"`
mkdir -p edb1/mysql-data/$dname
mydumper -h 127.0.0.1 -u root  --password=mypass --database=employees \
         --threads=7 --chunk-filesize 512 \
        --outputdir edb1/mysql-data/$dname
echo "...DONE"

echo "Syncing to S3"
aws s3 sync edb1/mysql-data/$dname s3://devgraph-devspaces-demos/dockerdb/edb1/mysql-data/$dname
