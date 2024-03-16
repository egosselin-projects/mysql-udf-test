#!/bin/bash

if [ -n "$MYSQL_ROOT_PASSWORD" ] ; then

	TEMP_FILE='/tmp/mysql-first-time.sql'
	cat > "$TEMP_FILE" <<-EOSQL
		-- setting up root password
		DELETE FROM mysql.user WHERE user = 'root' AND host = '%';
		CREATE USER 'root'@'%' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}' ;
		GRANT ALL ON *.* TO 'root'@'%' WITH GRANT OPTION ;
		FLUSH PRIVILEGES ;

		-- default database
		create database if not exists ${MYSQL_DATABASE} ;

		-- registering custom rest functions
		create function http_get returns string soname 'mysql-udf-http.so';
		create function http_post returns string soname 'mysql-udf-http.so';
		create function http_put returns string soname 'mysql-udf-http.so';
		create function http_delete returns string soname 'mysql-udf-http.so';
	EOSQL

	# setting init file
	set -- "$@" --init-file="$TEMP_FILE"
fi

exec "$@"