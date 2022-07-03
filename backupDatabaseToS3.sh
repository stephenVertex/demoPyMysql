#1/bin/bash

#echo "Stopping Docker mysql-server cleanly..."
#docker exec mysql-server /usr/bin/mysqladmin -uroot -pmypass shutdown
#echo "...DONE"

echo "Archiving up Docker volume..."
#./docker-backup-volume/backup-volume.sh -v mysql-data -p edb1
docker exec mysql-server /usr/bin/mysqldump -u root --password=mypass employees | gzip -9 -c > `date +"%Y-%m-%d_%H%M%S"`__backup.sql.gz
echo "...DONE"

echo "Archive information:"
export FNAME=edb1/mysql-data/`ls -t edb1/mysql-data/ | head -1`
ls -lh $FNAME

echo "Syncing to S3"
aws s3 sync edb1/ s3://devgraph-devspaces-demos/dockerdb/edb1
