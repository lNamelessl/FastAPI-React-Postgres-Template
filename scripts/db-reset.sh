#!/bin/bash

# Reset database (WARNING: Deletes all data!)

set -e

echo "⚠️  WARNING: This will delete all database data!"
read -p "Are you sure? Type 'yes' to confirm: " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

echo "Resetting database..."

cd backend

# Downgrade to base
echo "  Removing all migrations..."
uv run alembic downgrade base

# Upgrade to head
echo "  Recreating schema..."
uv run alembic upgrade head

cd ..

echo "✅ Database reset complete!"
