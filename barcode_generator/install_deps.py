import subprocess
import os
import sys

def install_barcode_dependencies():
    """
    Validate and install required packages.
    This function can be called manually or as a hook.
    """
    # Get the correct path to requirements.txt - it's in the app root
    app_path = os.path.dirname(os.path.dirname(__file__))  # Go up two levels from install_deps.py
    req_path = os.path.join(app_path, 'requirements.txt')
    
    if not os.path.exists(req_path):
        print(f"[Barcode Generator] Requirements file not found at: {req_path}")
        print(f"[Barcode Generator] App path: {app_path}")
        # Try alternative path
        alt_req_path = os.path.join(os.path.dirname(app_path), 'requirements.txt')
        if os.path.exists(alt_req_path):
            req_path = alt_req_path
            print(f"[Barcode Generator] Found requirements.txt at: {req_path}")
        else:
            print(f"[Barcode Generator] Alternative path also not found: {alt_req_path}")
            # Try installing manually with known requirements
            install_known_requirements()
            return
    
    print("[Barcode Generator] Validating dependencies...")
    
    # Read requirements
    try:
        with open(req_path, 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print(f"[Barcode Generator] Found {len(requirements)} requirements: {requirements}")
    except Exception as e:
        print(f"[Barcode Generator] Failed to read requirements: {e}")
        install_known_requirements()
        return
    
    # Check which packages are missing
    missing_packages = []
    for req in requirements:
        package_name = req.split('>=')[0].split('==')[0].split('<')[0].strip()
        # Handle package name variations
        import_name = package_name.replace('-', '_')
        if package_name == 'python-barcode':
            import_name = 'barcode'
        elif package_name == 'Pillow':
            import_name = 'PIL'
        
        try:
            __import__(import_name)
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

def install_known_requirements():
    """Install known requirements if requirements.txt is not found"""
    known_requirements = [
        "reportlab>=4.0.4",
        "python-barcode>=0.15.1", 
        "Pillow>=10.2.0",
        "qrcode>=7.4.2"
    ]
    
    print("[Barcode Generator] Installing known requirements...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + known_requirements)
        print("[Barcode Generator] ✅ Known requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"[Barcode Generator] ❌ Failed to install known requirements: {e}")
        raise

if __name__ == "__main__":
    # Allow running this script directly
    install_barcode_dependencies()
