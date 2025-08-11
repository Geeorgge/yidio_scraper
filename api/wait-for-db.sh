#!/bin/sh

# Get the database host from the first argument
host="$1"
shift

# Wait until the MySQL is available
until nc -z -v -w30 "$host" 3306
do
  echo "Waiting for the MySQL DB in the host $host..."
  sleep 1
done

echo "✅ MySQL is available at $host:3306"

# Run migrations (optional — only if you always want them)
python manage.py migrate

# Run the remaining command
exec "$@"
