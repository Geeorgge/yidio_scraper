#!/bin/sh

# Wait until the MySQL are available
until nc -z -v -w30 $1 3306
do
  echo "Waiting for the MySQL DB in the host $1..."
  sleep 1
done

echo "MySQL is available dude!!!"

# Run migrations
python manage.py migrate

# Execute the script
shift
exec "$@"
