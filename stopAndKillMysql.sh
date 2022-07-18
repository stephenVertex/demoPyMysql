#!/bin/bash

docker stop mysql-server
docker rm mysql-server
docker volume ls
docker volume rm mysql-data
