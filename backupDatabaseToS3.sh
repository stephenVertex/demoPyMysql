#1/bin/bash

echo "Stopping Docker mysql-server"
docker stop mysql-server
echo "...DONE"

echo "Archiving up Docker volume"
./docker-backup-volume/backup-volume.sh -v mysql-data -p edb1
echo "...DONE"

echo "Archive information:"
export FNAME=edb1/mysql-data/`ls -t edb1/mysql-data/ | head -1`
ls -lh $FNAME

echo "Syncing to S3"
aws s3 sync edb1/ s3://devgraph-devspaces-demos/dockerdb/edb1
