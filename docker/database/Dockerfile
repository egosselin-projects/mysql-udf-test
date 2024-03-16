# base image
FROM ubuntu:22.04

# installing mysql
RUN apt-get update && \
    apt-get install -y mysql-server

# installing build tools
RUN apt-get install -y make gcc libmysqlclient-dev pkg-config wget git libcurl4-openssl-dev

RUN git clone https://github.com/egosselin-dev/mysql-udf-http.git

# setting file permissions
RUN cd mysql-udf-http && chmod +x configure 

RUN cd mysql-udf-http && ./configure --with-mysql=/usr/bin/mysql_config && \
    make && make install && \
    cd ../

# copying generated library to mysql plugin directory
RUN cp /mysql-udf-http/src/.libs/mysql-udf-http.so /usr/lib/mysql/plugin/

EXPOSE 3306

# adding entrypoint to register custom mysql functions
ADD ./entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Change mysql to listen on 0.0.0.0 (otherwise you can't connect from outside)
RUN sed -i 's/127\.0\.0\.1/0.0.0.0/g' /etc/mysql/mysql.conf.d/mysqld.cnf

CMD ["mysqld"]