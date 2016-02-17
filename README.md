# AWS CodeDeploy Simple setting for Django Framework
Configuration Example for Django server deploy automation on AWS using AWS [CodeDeploy](https://aws.amazon.com/codedeploy/)

## How it works
  - We assume that we are going to deploy a **staging** environment!
  - appspec.yml file is used to specify shell scripts(scripts/*.sh) to run on each step.
  - [django rest framework](http://www.django-rest-framework.org/) is used.
  - static files are saved in S3 on this **staging** environment.
  - we use Nginx as a web server.
  - [supervisor](http://supervisord.org/) is used to control a process
  - CodeDeploy scripts(appspec.yml, scripts/*.sh) control all of above.

## Prerequisites
- We need a S3 bucket of this project. Read more about [s3](https://aws.amazon.com/s3/)
- We need a Postgres RDS server on a private subnet. Read more about [RDS](https://aws.amazon.com/rds/) and [VPC](https://aws.amazon.com/vpc/)
- We need a amazon linux ec2 instance with a role of AmazonS3FullAccess to a given bucket in the same VPC of RDS server. Read more about [ec2 roles](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html)

## Checklist
In ```scripts/migrate.sh```
```bash
DJANGO_SETTINGS_MODULE=project.settings.staging SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 ./manage.py makemigrations
DJANGO_SETTINGS_MODULE=project.settings.staging SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 ./manage.py migrate auth
DJANGO_SETTINGS_MODULE=project.settings.staging SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 ./manage.py migrate
```
Please set SECRET_KEY, JWT_SECRET_KEY, PSQL_DB_NAMEPSQL_DB_USER, PSQL_DB_PASSWD, PSQL_HOST to your values.
**This is just an EXAMPLE, so Please DO NOT commit above credentials in a public repository. We MUST store those values in a non-public S3 bucket, and ec2 can access them with a given access role.**

In ```scripts/start_application.sh```
```bash
echo yes | DJANGO_SETTINGS_MODULE=project.settings.staging SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 /home/ec2-user/www/project/manage.py collectstatic
DJANGO_SETTINGS_MODULE=project.settings.staging SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 supervisord -c /home/ec2-user/www/project/supervisor/default.conf
```
Please set SECRET_KEY, JWT_SECRET_KEY, PSQL_DB_NAMEPSQL_DB_USER, PSQL_DB_PASSWD, PSQL_HOST to your values.

In ```supervisor/default.conf``` line 60:
```bash
[program:run_django]
environment=DJANGO_SETTINGS_MODULE=%(ENV_DJANGO_SETTINGS_MODULE)s,SECRET_KEY=%(ENV_SECRET_KEY)s,JWT_SECRET_KEY=%(ENV_JWT_SECRET_KEY)s,S3_BUCKET_NAME=%(ENV_S3_BUCKET_NAME)s,PSQL_DB_NAME=%(ENV_PSQL_DB_NAME)s,PSQL_DB_USER=%(ENV_PSQL_DB_USER)s,PSQL_DB_PASSWD=%(ENV_PSQL_DB_PASSWD)s,PSQL_HOST=%(ENV_PSQL_HOST)s,PSQL_PORT=%(ENV_PSQL_PORT)s
```

Make sure that all environment values have a format like:

VALUE=%(ENV_VALUE)s,ANOTHER_VALUE=%(ENV_ANOTHER_VALUE)s,etc...
