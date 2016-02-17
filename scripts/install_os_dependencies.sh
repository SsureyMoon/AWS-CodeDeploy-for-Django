#!/usr/bin/env bash
yum install -y python-psycopg2 postgresql libncurses5-dev libffi libffi-devel libxml2-devel libxslt-devel libxslt1-dev
yum install -y postgresql-libs postgresql-devel python-lxml python-devel gcc patch python-setuptools
yum install -y gcc-c++ flex epel-release nginx supervisor
/etc/init.d/nginx stop