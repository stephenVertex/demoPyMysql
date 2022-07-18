#!/bin/bash

docker run -d --name=mysql-server -p 3306:3306 \
        -e MYSQL_ROOT_PASSWORD=mypass       \
        -e MYSQL_DATABASE=testdb            \
        -v mysql-data:/var/lib/mysql        \
        -v `pwd`/test_db:/test_db           \
        mysql:8.0.29 --max-allowed-packet=67108864 

