from fabric.api import local
from fabric.decorators import task

postgres_dir = "/usr/local/var/postgres"
postgres_log = "/usr/local/var/postgres/server.log"


@task
def run_db_on_mac():
    local("pg_ctl -D {} -l {} start".format(postgres_dir, postgres_log), capture=False)
