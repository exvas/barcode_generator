# ========================================
# STEP 1: Create this file: barcode_generator/barcode_generator/install.py
# ========================================

import subprocess
import sys
import importlib.util

def before_install():
    """Install packages BEFORE app installation"""
    print("🔧 Auto-installing barcode packages...")
    
    packages_to_install = [
        "reportlab>=4.0.4",
        "python-barcode>=0.15.1", 
        "Pillow>=10.2.0",
        "qrcode>=7.4.2"
    ]
    
    # Check and install packages
    for package in packages_to_install:
        package_name = package.split(">=")[0]
        check_name = {
            "reportlab": "reportlab",
            "python-barcode": "barcode",
            "Pillow": "PIL", 
            "qrcode": "qrcode"
        }.get(package_name, package_name)
        
        try:
            importlib.import_module(check_name)
            print(f"✅ {package_name} - already installed")
        except ImportError:
            print(f"📦 Installing {package_name}...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], check=True, capture_output=True, text=True)
                print(f"✅ {package_name} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package_name}: {e}")
    
    print("✅ Package installation completed!")

def after_install():
    """Called after app installation"""
    print("✅ Barcode Generator app installed successfully!")

# ========================================
# STEP 2: Fix your hooks.py file - CHANGE THIS LINE:
# ========================================

# In your barcode_generator/barcode_generator/hooks.py file
# FIND this line:
# before_install = "barcode_generator.install_deps.before_install"

# CHANGE it to:
# before_install = "barcode_generator.install.before_install"

# AND FIND this line:
# after_install = "barcode_generator.install_deps.after_install"

# CHANGE it to:
# after_install = "barcode_generator.install.after_install"