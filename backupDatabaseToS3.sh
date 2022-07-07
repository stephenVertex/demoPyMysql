#!/bin/bash
# File: backupDatabaseToS3.sh
#
# Usage: Run this script from the root directory:
# $ cd ~
# $ ./backupDatabaseToS3.sh
#

echo "Backing Up Database..."
dname=`date +"%Y-%m-%d_%H%M%S"`
mkdir -p edb1/mysql-data/$dname
mydumper -h 127.0.0.1 -u root  --password=mypass --database=employees \
         --threads=7 --chunk-filesize 512 \
        --outputdir edb1/mysql-data/$dname
echo "...DONE"

echo "Syncing to S3"
aws s3 sync edb1/mysql-data/$dname s3://devgraph-devspaces-demos/dockerdb/edb1/mysql-data/$dname
