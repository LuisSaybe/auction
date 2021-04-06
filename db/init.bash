#!/bin/bash
set -e

psql -f /docker-entrypoint-initdb.d/create.sql