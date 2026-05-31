#!/bin/sh
# wait-for-db.sh

set -e

host="$1"
shift
cmd="$@"

# Use pg_isready, a PostgreSQL client tool, to check the database status.
# We will loop until the database is ready to accept commands.
until pg_isready -h "$host" -p "5432" -U "docqure_user"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd