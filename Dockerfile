FROM ubuntu:16.04

MAINTAINER Vyacheslav Kruglov

# Обвновление списка пакетов
RUN apt-get -y update

#
# Установка postgresql
#
ENV PGVER 9.5
RUN apt-get install -y postgresql-$PGVER

# Run the rest of the commands as the ``postgres`` user created by the ``postgres-$PGVER`` package when it was ``apt-get installed``
USER postgres

# Create a PostgreSQL role named ``docker`` with ``docker`` as the password and
# then create a database `docker` owned by the ``docker`` role.
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -E UTF8 -T template0 -O docker docker &&\
    /etc/init.d/postgresql stop

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/$PGVER/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/$PGVER/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/$PGVER/main/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Back to the root user
USER root

#
# Сборка проекта
#

# Установка Python
RUN apt-get install -y python
RUN apt-get install -y django
RUN apt-get install -y python-pip
RUN apt-get install -y gunicorn
RUN pip install pytz
RUN pip install psycopg2

# Копируем исходный код в Docker-контейнер
ENV WORK /opt/TechnoparkDB
ADD dbAPI/ $WORK/dbAPI/
ADD start.sh $WORK/start.sh
ADD schema.sql $WORK/schema.sql

# Собираем и устанавливаем пакет
#WORKDIR $WORK/
#RUN mvn package

# Объявлем порт сервера
EXPOSE 5000

# Создаем базу
RUN $WORK/start.sh

#
# Запускаем PostgreSQL и сервер
#
CMD service postgresql start && gunicorn -b :5000 $WORK/dbAPI/dbAPI.wsgi
