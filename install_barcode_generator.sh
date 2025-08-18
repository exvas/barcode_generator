#!/bin/bash

# ========================================
# Barcode Generator - Auto Installation Script
# Automatically installs dependencies and the app
# ========================================

set -e  # Exit on any error

echo "🚀 Barcode Generator - Auto Installation"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in a Frappe bench directory
if [ ! -f "common_site_config.json" ]; then
    print_error "This script must be run from a Frappe bench directory"
    print_error "Please cd to your frappe-bench directory first"
    exit 1
fi

print_status "Found Frappe bench directory ✓"

# Check if virtual environment exists
if [ ! -f "env/bin/activate" ]; then
    print_error "Virtual environment not found at env/bin/activate"
    print_error "Make sure you're in the correct frappe-bench directory"
    exit 1
fi

print_status "Activating virtual environment..."
source env/bin/activate

# Install Python dependencies
print_status "Installing required Python packages..."

PACKAGES=(
    "reportlab>=4.0.4"
    "python-barcode>=0.15.1"
    "Pillow>=10.2.0"
    "qrcode>=7.4.2"
    "pandas>=1.3.0"
    "openpyxl>=3.0.0"
)

# Install all packages
for package in "${PACKAGES[@]}"; do
    package_name=$(echo "$package" | cut -d'>' -f1 | cut -d'=' -f1)
    print_status "Installing $package_name..."
    
    if pip install "$package"; then
        print_success "$package_name installed successfully"
    else
        print_warning "Failed to install $package_name, but continuing..."
    fi
done

# Get the barcode generator app if not already present
if [ ! -d "apps/barcode_generator" ]; then
    print_status "Getting barcode_generator app..."
    if bench get-app https://github.com/exvas/barcode_generator.git; then
        print_success "Barcode generator app downloaded successfully"
    else
        print_error "Failed to download barcode generator app"
        exit 1
    fi
else
    print_status "Barcode generator app already exists, skipping download"
fi

# Ask for site name
echo ""
print_status "Available sites:"
ls sites/ | grep -v common_site_config.json | grep -v assets

echo ""
read -p "Enter the site name to install the app on: " SITE_NAME

if [ -z "$SITE_NAME" ]; then
    print_error "Site name cannot be empty"
    exit 1
fi

if [ ! -d "sites/$SITE_NAME" ]; then
    print_error "Site '$SITE_NAME' does not exist"
    exit 1
fi

# Install the app
print_status "Installing barcode_generator app on site '$SITE_NAME'..."
if bench --site "$SITE_NAME" install-app barcode_generator; then
    print_success "App installed successfully!"
else
    print_error "Failed to install app"
    exit 1
fi

# Run migration to ensure all tables are created
print_status "Running database migration..."
bench --site "$SITE_NAME" migrate

# Clear cache
print_status "Clearing cache..."
bench --site "$SITE_NAME" clear-cache

# Build assets
print_status "Building assets..."
bench build --app barcode_generator

print_success "🎉 Installation completed successfully!"
echo ""
echo "======================================"
print_success "🏷️  BARCODE GENERATOR READY TO USE!"
echo "======================================"
echo "📍 Access at: http://$SITE_NAME:8000"
echo "📋 Navigate to: Modules > Barcode Generator > Bulk Barcode Generator"
echo ""
echo "✨ Features available:"
echo "   • Upload CSV/Excel files with barcode data"
echo "   • Download sample templates"
echo "   • Generate bulk barcodes (Code128, EAN13, etc.)"
echo "   • Support for thermal labels (50x25mm)"
echo "   • High-density layouts for A4/Letter printing"
echo ""
print_status "Need help? Check the GitHub repository: https://github.com/exvas/barcode_generator"
echo ""
