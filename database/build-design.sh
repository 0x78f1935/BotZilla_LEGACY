#!/bin/bash

ENV=`mktemp -d`
trap 'rm -rf $ENV' EXIT

virtualenv --python=python3 $ENV
{
    . $ENV/bin/activate
    python --version
    pip install git+git://github.com/hendrikx-itc/pg-db-tools
    compile-db-schema sql --if-not-exists design/schema-design.yml > src/00_base.sql
}

exit 0

