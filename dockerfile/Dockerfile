FROM postgres:10

LABEL maintainer="Daniil Shadrin rabbit72rus@gmail.com"

# users/password in image
#ENV POSTGRES_USER postgres
#ENV POSTGRES_PASSWORD docker
#ENV POSTGRES_DB docker

ADD migrations/01_сreate.sql /docker-entrypoint-initdb.d/
