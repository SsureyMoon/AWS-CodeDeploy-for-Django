#!/usr/bin/env bash

cd /home/ec2-user/www/project/
source /home/ec2-user/www/project-venv/bin/activate
echo yes | DJANGO_SETTINGS_MODULE=project.settings.staging SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 /home/ec2-user/www/project/manage.py collectstatic
DJANGO_SETTINGS_MODULE=project.settings.staging SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 supervisord -c /home/ec2-user/www/project/supervisor/default.conf