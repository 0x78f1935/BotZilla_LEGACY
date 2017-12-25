#!/bin/bash

export GIS_DB_NAME=gis
export PGDATABASE=$GIS_DB_NAME
export PGUSER=postgres

/bi-bricks/scripts/create-database
