import subprocess
import os
import sys
import importlib.util

def before_install():
    """Install packages BEFORE app installation starts"""
    try:
        print("🚀 Barcode Generator: Installing required packages before app installation...")
        print("📋 This may take a few minutes...")
        
        # Try to install from requirements.txt first
        try:
            requirements_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                'requirements.txt'
            )
            if os.path.exists(requirements_path):
                print(f"📦 Installing from requirements.txt: {requirements_path}")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", requirements_path,
                    "--upgrade", "--no-cache-dir", "--timeout", "300"
                ], check=True, timeout=600)
                print("✅ Requirements installed from requirements.txt")
            else:
                print("⚠️ requirements.txt not found, installing packages individually...")
                # Fallback to individual package installation
                install_required_packages()
        except Exception as e:
            print(f"⚠️ Requirements.txt installation failed: {str(e)}")
            print("🔄 Falling back to individual package installation...")
            install_required_packages()
        
        # Verify installation
        verification_result = verify_and_reinstall_packages()
        if verification_result:
            print("✅ Pre-installation package setup completed successfully!")
        else:
            print("⚠️ Some packages may not be properly installed. The app will use fallback methods.")
        
    except Exception as e:
        print(f"❌ Pre-installation failed: {str(e)}")
        print("📋 Manual installation required. Please run:")
        print("   ./env/bin/pip install reportlab>=4.0.4 python-barcode>=0.15.1 Pillow>=10.2.0 qrcode>=7.4.2")
        # Don't raise exception here to allow installation to continue

def after_install():
    """Run after app installation"""
    try:
        print("Starting Barcode Generator post-installation setup...")

        # Verify packages are installed (reinstall if needed)
        verify_and_reinstall_packages()

        print("Barcode Generator installation completed successfully!")

    except Exception as e:
        print(f"Installation failed: {str(e)}")

def install_required_packages():
    """Install required Python packages with better error handling"""
    packages = [
        'reportlab>=4.0.4',
        'python-barcode>=0.15.1', 
        'Pillow>=10.2.0',
        'qrcode>=7.4.2'
    ]
    
    print("Installing required Python packages...")
    
    # Check if we're in a virtual environment
    virtual_env = os.environ.get('VIRTUAL_ENV')
    if virtual_env:
        print(f"✓ Using virtual environment: {virtual_env}")
    
    failed_packages = []
    
    # Install packages one by one with retries
    for package in packages:
        package_name = package.split('>=')[0].split('==')[0]  # Extract package name
        try:
            # First check if package is already installed
            if is_package_installed(package_name):
                print(f"✓ {package_name} already installed")
                continue
                
            print(f"Installing {package}...")
            
            # Use pip install with more robust options
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package, 
                "--upgrade", "--no-cache-dir", "--force-reinstall"
            ], capture_output=True, text=True, check=True, timeout=600)
            
            print(f"✓ {package} installed successfully")
            
            # Verify installation immediately
            if not is_package_installed(package_name):
                raise Exception(f"Package {package_name} installation verification failed")
                
        except subprocess.TimeoutExpired:
            error_msg = f"Installation timeout for {package}"
            print(f"✗ {error_msg}")
            failed_packages.append(package_name)
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to install {package}: {e.stderr if e.stderr else str(e)}"
            print(f"✗ {error_msg}")
            failed_packages.append(package_name)
            
        except Exception as e:
            error_msg = f"Error installing {package}: {str(e)}"
            print(f"✗ {error_msg}")
            failed_packages.append(package_name)
    
    if failed_packages:
        print(f"\n⚠️  Warning: Failed to install packages: {', '.join(failed_packages)}")
        print("Manual installation commands:")
        for pkg in failed_packages:
            print(f"  ./env/bin/pip install {pkg} --upgrade --no-cache-dir")
        print("\nAlternatively, run from your bench directory:")
        print("  ./env/bin/pip install -r apps/barcode_generator/requirements.txt")

def verify_and_reinstall_packages():
    """Verify packages and reinstall if needed"""
    print("Verifying package installations...")
    
    packages_to_check = {
        'reportlab': 'reportlab',
        'python-barcode': 'barcode',
        'Pillow': 'PIL',
        'qrcode': 'qrcode'
    }
    
    missing_packages = []
    
    for package, import_name in packages_to_check.items():
        try:
            if import_name == 'reportlab':
                import reportlab
                print(f"✓ {package} verified (version: {reportlab.Version})")
            elif import_name == 'barcode':
                import barcode
                print(f"✓ {package} verified")
            elif import_name == 'PIL':
                import PIL
                print(f"✓ {package} verified (version: {PIL.__version__})")
            elif import_name == 'qrcode':
                import qrcode
                print(f"✓ {package} verified (version: {qrcode.__version__})")
        except ImportError:
            print(f"✗ {package} not available")
            missing_packages.append(package)
        except Exception as e:
            print(f"✗ {package} verification error: {str(e)}")
            missing_packages.append(package)
    
    # Reinstall missing packages
    if missing_packages:
        print(f"Reinstalling missing packages: {', '.join(missing_packages)}")
        for package in missing_packages:
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", package, 
                    "--upgrade", "--force-reinstall", "--no-cache-dir"
                ], check=True, timeout=300)
                print(f"✓ {package} reinstalled")
            except Exception as e:
                print(f"✗ Failed to reinstall {package}: {str(e)}")
                
    return len(missing_packages) == 0

def is_package_installed(package_name):
    """Check if a Python package is installed and importable"""
    try:
        # Handle package name variations
        if package_name == 'python-barcode':
            import barcode
            return True
        elif package_name == 'Pillow':
            import PIL
            return True
        else:
            spec = importlib.util.find_spec(package_name)
            return spec is not None
    except ImportError:
        return False
    except Exception:
        return False

def install_barcode_dependencies():
    """
    Legacy function for backward compatibility.
    This function can be called manually or as a hook.
    """
    verify_and_reinstall_packages()

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
