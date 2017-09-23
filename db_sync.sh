#!/usr/bin/env bash

# Retrieve postgresql backup from server
echo "retrieving db backup from server..."
scp harshp.com:~/backup/harshp_com_db_backup.sql /tmp/harshp_com_db_backup.sql
if [ $? -eq 0 ]; then
    echo "success!"
else
    rm /tmp/harshp_com_db_backup.sql
    echo "failed!"
    exit -1
fi

# Clear existing database
psql -U postgres -c "drop database if exists harshp_com;"
psql -U postgres -c "create database \"harshp_com\";"
psql -U postgres -c "grant all privileges on database \"harshp_com\" to harshp_db_admin;"
sudo -u postgres pg_restore -U harshp_db_admin -d harshp_com -v \
    /tmp/harshp_com_db_backup.sql
rm /tmp/harshp_com_db_backup.sql
echo "updated database"

# Apply any unapplied migrations
# python3 harshp_com/manage.py migrate

exit 0
