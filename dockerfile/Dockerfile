FROM postgres:10

LABEL maintainer="Daniil Shadrin rabbit72rus@gmail.com"

RUN apt-get update
RUN apt-get install -y libcurl4-openssl-dev wget


# Install zombo
RUN wget --quiet https://www.zombodb.com/releases/v10-1.0.0b4/zombodb_jessie_pg10-10-1.0.0b4_amd64.deb

RUN dpkg -i zombodb_jessie_pg10-10-1.0.0b4_amd64.deb

# add wait
COPY wait-for-it.sh /usr/local/bin/
RUN chmod 777 /usr/local/bin/wait-for-it.sh

# create tables
ADD migrations/00-create_functions.sql /docker-entrypoint-initdb.d/
ADD migrations/01-сreate_author.sql /docker-entrypoint-initdb.d/
ADD migrations/02-create_book.sql /docker-entrypoint-initdb.d/
ADD migrations/03-create_book_author.sql /docker-entrypoint-initdb.d/
