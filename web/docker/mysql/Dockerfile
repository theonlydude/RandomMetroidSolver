FROM mysql:5.7

ADD create_schema.sql /docker-entrypoint-initdb.d/create_schema.sql
ADD create_extended_stats.sql /docker-entrypoint-initdb.d/create_extended_stats.sql
ADD dump.sql /docker-entrypoint-initdb.d/dump.sql
