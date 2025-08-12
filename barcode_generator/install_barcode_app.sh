#!/bin/bash

SITE_NAME=$1

if [ -z "$SITE_NAME" ]; then
    echo "Usage: $0 <site-name>"
    exit 1
fi

echo "Installing Barcode Generator App for site: $SITE_NAME"

# Install system dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3-dev libjpeg-dev zlib1g-dev libfreetype6-dev


# Activate virtual environment and install Python packages
echo "Installing Python dependencies..."
if [ -d "../../.venv" ]; then
    source ../../.venv/bin/activate
elif [ -d "../../../.venv" ]; then
    source ../../../.venv/bin/activate
elif [ -d "env" ]; then
    source env/bin/activate
else
    echo "No virtual environment found. Please create one before running this script."
    exit 1
fi
pip install -r ../../requirements.txt

# Verify installation
echo "Verifying package installation..."
python -c "import reportlab, barcode, qrcode; print('✅ All packages verified')"

# Install app to site
echo "Installing app to site..."
bench --site $SITE_NAME install-app barcode_generator

# Migrate database
echo "Running migrations..."
bench --site $SITE_NAME migrate

# Clear cache and restart
echo "Clearing cache and restarting..."
bench --site $SITE_NAME clear-cache
bench restart

echo "✅ Barcode Generator App installed successfully!"
echo "You can now access it at: http://your-domain/app/bulk-barcode-generator"