#!/bin/bash
# File: backupDatabaseToS3.sh
#
# Usage: Run this script from the root directory:
# $ cd ~
# $ ./backupDatabaseToS3.sh
#

echo "Stopping Docker mysql-server cleanly..."
docker exec mysql-server /usr/bin/mysqladmin -uroot -pmypass shutdown
echo "...DONE"

echo "Archiving up Docker volume..."
./docker-backup-volume/backup-volume.sh -v mysql-data -p edb1
echo "...DONE"

echo "Archive information:"
export FNAME=edb1/mysql-data/`ls -t edb1/mysql-data/ | head -1`
ls -lh $FNAME

echo "Syncing to S3"
aws s3 sync edb1/ s3://devgraph-devspaces-demos/dockerdb/edb1