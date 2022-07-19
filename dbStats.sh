#!/bin/bash

mysql -t -u root -pmypass -h 127.0.0.1 < dbsummary.sql
