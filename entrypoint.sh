#!/bin/sh

# Wait for the PostgreSQL database to be available
while ! pg_isready -h $POSTGRES_HOST -p 5432 -d $POSTGRES_DB -U $POSTGRES_USER; do
    echo "$(date) - Waiting for the PostgreSQL server at $POSTGRES_HOST:$POSTGRES_PORT"
    sleep 3
done

echo "$(date) - PostgreSQL is available, proceeding with migrations"

# Run database migrations
python manage.py migrate

# Run the Django server
exec "$@"
