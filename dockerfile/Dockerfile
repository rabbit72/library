FROM postgres:10

LABEL maintainer="Daniil Shadrin rabbit72rus@gmail.com"

# users/password in image
#ENV POSTGRES_USER postgres
#ENV POSTGRES_PASSWORD docker
#ENV POSTGRES_DB docker

ADD migrations/00-create_functions.sql /docker-entrypoint-initdb.d/
ADD migrations/01-сreate_author.sql /docker-entrypoint-initdb.d/
ADD migrations/02-create_book.sql /docker-entrypoint-initdb.d/
ADD migrations/03-create_book_author.sql /docker-entrypoint-initdb.d/
