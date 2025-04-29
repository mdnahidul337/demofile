#!/bin/bash

# Exit on error
set -e

echo "Starting Flask project deployment..."

# Optional: Activate Python virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Optional: Export Flask app environment variables
echo "Setting Flask environment variables..."
export FLASK_APP=app.py      # Change to your main app file
export FLASK_ENV=production  # or 'development'

# Optional: Run database migrations if using Flask-Migrate
# echo "Running database migrations..."
# flask db upgrade

# Start the server (using Flask’s dev server or production WSGI server)
echo "Starting Flask server..."
flask run --host=0.0.0.0 --port=5000

# For production, consider using gunicorn instead:
# gunicorn -w 4 -b 0.0.0.0:5000 app:app

echo "Deployment complete."
