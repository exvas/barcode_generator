import subprocess
import os
import sys

def install_barcode_dependencies():
    """
    Validate and install required packages before app installation.
    Checks if packages are already installed, installs missing ones.
    """
    req_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../requirements.txt'))
    
    if not os.path.exists(req_path):
        print(f"[Barcode Generator] Requirements file not found: {req_path}")
        return
    
    print("[Barcode Generator] Validating dependencies...")
    
    # Read requirements
    try:
        with open(req_path, 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except Exception as e:
        print(f"[Barcode Generator] Failed to read requirements: {e}")
        return
    
    # Check which packages are missing
    missing_packages = []
    for req in requirements:
        package_name = req.split('>=')[0].split('==')[0].split('<')[0].strip()
        try:
            __import__(package_name.replace('-', '_'))
            print(f"[Barcode Generator] ✓ {package_name} already installed")
        except ImportError:
            missing_packages.append(req)
            print(f"[Barcode Generator] ✗ {package_name} not found")
    
    # Install missing packages
    if missing_packages:
        print(f"[Barcode Generator] Installing {len(missing_packages)} missing packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("[Barcode Generator] ✅ All dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"[Barcode Generator] ❌ Failed to install dependencies: {e}")
            raise
    else:
        print("[Barcode Generator] ✅ All dependencies already satisfied")
