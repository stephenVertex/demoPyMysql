#!/bin/bash
# File: backupDatabaseToS3.sh
#
# Usage: Run this script from the root directory:
# $ cd ~
# $ ./backupDatabaseToS3.sh
#

echo "Flushing SQL tables"
docker exec mysql-server /usr/bin/mysql -u root -pmypass -e 'flush tables;'

echo "Stopping Docker mysql-server cleanly..."
docker exec mysql-server /usr/bin/mysqladmin -uroot -pmypass shutdown
echo "...DONE"

echo "Archiving up Docker volume..."
# ./docker-backup-volume/backup-volume.sh -v mysql-data -p edb1
# 
export FD=`date +"%Y-%m-%d_%H%M%S"`
sudo chown -R gitpod:gitpod mysql-data/
aws s3 cp --recursive  mysql-data s3://devgraph-devspaces-demos/dockerdb/edb1/$FD
echo "...DONE"


echo "DONE:"
echo $FD
du -h -d 1 mysql-data
