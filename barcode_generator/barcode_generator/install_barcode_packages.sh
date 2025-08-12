#!/bin/bash

# ========================================
# Barcode Generator Package Installer
# Works on Mac and Ubuntu
# ========================================

set -e  # Exit on any error

echo "🚀 Barcode Generator Package Installer"
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

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

print_status "Detected OS: $MACHINE"

# Find frappe-bench directory
BENCH_DIR=""
if [ -d "frappe-bench" ]; then
    BENCH_DIR="frappe-bench"
elif [ -d "../frappe-bench" ]; then
    BENCH_DIR="../frappe-bench"
elif [ -d "~/frappe-bench" ]; then
    BENCH_DIR="~/frappe-bench"
else
    print_warning "Frappe bench directory not found. Using current directory."
    BENCH_DIR="."
fi

print_status "Using bench directory: $BENCH_DIR"

# Navigate to frappe bench
cd "$BENCH_DIR" || {
    print_error "Failed to navigate to $BENCH_DIR"
    exit 1
}

# Check if virtual environment exists
if [ ! -f "env/bin/activate" ]; then
    print_error "Virtual environment not found at env/bin/activate"
    print_error "Make sure you're in the correct frappe-bench directory"
    exit 1
fi

print_status "Activating virtual environment..."
source env/bin/activate

# Check if pip is available
if ! command -v pip &> /dev/null; then
    print_error "pip not found in virtual environment"
    exit 1
fi

print_success "Virtual environment activated"

# Install packages
print_status "Installing barcode packages..."

PACKAGES=(
    "reportlab>=4.0.4"
    "python-barcode>=0.15.1"
    "Pillow>=10.2.0"
    "qrcode>=7.4.2"
)

# Install all packages at once
print_status "Installing: ${PACKAGES[*]}"
if pip install "${PACKAGES[@]}"; then
    print_success "All packages installed successfully!"
else
    print_warning "Batch installation failed. Trying individual installation..."
    
    # Install packages one by one
    for package in "${PACKAGES[@]}"; do
        package_name=$(echo "$package" | cut -d'>' -f1)
        print_status "Installing $package_name..."
        
        if pip install "$package"; then
            print_success "$package_name installed"
        else
            print_error "Failed to install $package_name"
            print_status "Trying with --user flag..."
            if pip install --user "$package"; then
                print_success "$package_name installed with --user flag"
            else
                print_error "Failed to install $package_name even with --user flag"
            fi
        fi
    done
fi

# Verify installation
print_status "Verifying package installation..."

# Test imports
if python -c "import reportlab, barcode, PIL, qrcode; print('All packages imported successfully!')" 2>/dev/null; then
    print_success "✅ All packages are working correctly!"
else
    print_error "❌ Package verification failed"
    print_status "Checking individual packages..."
    
    # Check each package individually
    packages_check=("reportlab" "barcode" "PIL" "qrcode")
    for pkg in "${packages_check[@]}"; do
        if python -c "import $pkg; print('$pkg: OK')" 2>/dev/null; then
            print_success "$pkg: ✅ Working"
        else
            print_error "$pkg: ❌ Failed"
        fi
    done
fi

# Show installed versions
print_status "Installed package versions:"
pip list | grep -E "(reportlab|barcode|Pillow|qrcode)" || print_warning "Could not list package versions"

echo ""
echo "======================================"
print_success "🎉 Installation completed!"
echo "======================================"
echo ""
print_status "Next steps:"
echo "1. Install your barcode generator app:"
echo "   bench --site your-site-name install-app barcode_generator"
echo ""
echo "2. If you get any errors, restart your bench:"
echo "   bench restart"
echo ""
print_status "Happy coding! 🚀"