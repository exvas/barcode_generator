"""
Auto-installer for barcode_generator Frappe app
Create this file: barcode_generator/install.py
This runs BEFORE the app installs to the site
"""

import subprocess
import sys
import importlib.util
import frappe
from frappe import _

def before_install():
    """Called BEFORE app installation - auto-install packages here"""
    print("🔧 Installing required packages for Barcode Generator...")
    
    required_packages = [
        "reportlab>=4.0.4",
        "python-barcode>=0.15.1", 
        "Pillow>=10.2.0",
        "qrcode>=7.4.2"
    ]
    
    # Check what's missing
    missing_packages = []
    package_check_names = {
        "reportlab": "reportlab",
        "python-barcode": "barcode",
        "Pillow": "PIL", 
        "qrcode": "qrcode"
    }
    
    for package_spec in required_packages:
        package_name = package_spec.split(">=")[0]
        check_name = package_check_names.get(package_name, package_name)
        
        try:
            importlib.import_module(check_name)
            print(f"✅ {package_name} - already installed")
        except ImportError:
            print(f"❌ {package_name} - missing, will install")
            missing_packages.append(package_spec)
    
    # Install missing packages
    if missing_packages:
        try:
            print(f"📦 Installing {len(missing_packages)} packages...")
            
            for package in missing_packages:
                package_name = package.split(">=")[0]
                print(f"Installing {package_name}...", end=" ")
                
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], capture_output=True, text=True, check=True)
                
                print("✅")
            
            print("✅ All packages installed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print("❌")
            print(f"Failed to install packages: {e.stderr}")
            print("Manual installation required:")
            for pkg in missing_packages:
                print(f"  pip install {pkg}")
            return False
    else:
        print("✅ All required packages are already installed!")
        return True

def after_install():
    """Called after app installation"""
    print("✅ Barcode Generator app installed successfully!")
    
    # Verify packages are working
    try:
        import reportlab
        import barcode
        import PIL
        import qrcode
        print("✅ All barcode packages verified and working!")
    except ImportError as e:
        print(f"⚠️  Warning: Package verification failed: {e}")
        print("You may need to restart your bench.")