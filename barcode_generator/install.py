import frappe
import subprocess
import sys
import os

def get_requirements():
    """Get list of required packages"""
    return [
        "reportlab>=4.0.4",
        "python-barcode>=0.15.1", 
        "Pillow>=10.2.0",
        "qrcode>=7.4.2",
        "pandas>=1.3.0",
        "openpyxl>=3.0.0"
    ]

def install_dependencies():
    """Install required Python packages automatically"""
    try:
        print("🚀 Installing Barcode Generator dependencies...")
        
        # Get the current Python executable (respects virtual environments)
        python_executable = sys.executable
        
        requirements = get_requirements()
        
        for package in requirements:
            try:
                print(f"📦 Installing {package}...")
                
                # Use subprocess to install each package
                result = subprocess.run(
                    [python_executable, "-m", "pip", "install", package],
                    check=True,
                    capture_output=True,
                    text=True
                )
                
                print(f"✅ Successfully installed {package}")
                
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Warning: Failed to install {package}")
                print(f"Error: {e.stderr}")
                continue
            except Exception as e:
                print(f"⚠️  Warning: Unexpected error installing {package}: {str(e)}")
                continue
        
        # Verify installations
        print("\n🔍 Verifying installations...")
        verify_installations()
        
        print("✅ Barcode Generator dependencies installation completed!")
        
    except Exception as e:
        print(f"❌ Error during dependency installation: {str(e)}")
        # Don't fail the app installation if dependencies fail
        print("💡 You can manually install dependencies using:")
        print("pip install reportlab>=4.0.4 python-barcode>=0.15.1 Pillow>=10.2.0 qrcode>=7.4.2 pandas>=1.3.0 openpyxl>=3.0.0")

def verify_installations():
    """Verify that all packages are properly installed"""
    test_imports = [
        ("reportlab", "reportlab"),
        ("barcode", "python-barcode"),
        ("PIL", "Pillow"),
        ("qrcode", "qrcode"),
        ("pandas", "pandas"),
        ("openpyxl", "openpyxl")
    ]
    
    for import_name, package_name in test_imports:
        try:
            __import__(import_name)
            print(f"✅ {package_name}: OK")
        except ImportError:
            print(f"❌ {package_name}: Failed to import")

def before_install():
    """Hook called before app installation"""
    print("🔧 Preparing Barcode Generator installation...")
    print("📦 Installing required dependencies first...")
    
    # Install dependencies BEFORE app installation
    install_dependencies()
    
def after_install():
    """Hook called after app installation"""
    print("🎉 Barcode Generator installed successfully!")
    
    # Verify dependencies are still working after installation
    print("🔍 Final verification of dependencies...")
    verify_installations()
    
    # Create a welcome message
    print("\n" + "="*60)
    print("🏷️  BARCODE GENERATOR - INSTALLATION COMPLETE!")
    print("="*60)
    print("📍 Navigate to: Modules > Barcode Generator > Bulk Barcode Generator")
    print("📋 Features:")
    print("   • Upload CSV/Excel files")
    print("   • Download sample templates")  
    print("   • Generate bulk barcodes")
    print("   • Support for thermal labels (50x25mm)")
    print("   • Multiple barcode types (Code128, EAN13, etc.)")
    print("="*60)
    print("💡 Need help? Check the documentation or GitHub repository.")
    print("")

def before_uninstall():
    """Hook called before app uninstallation"""
    print("🗑️  Uninstalling Barcode Generator...")

def after_uninstall():
    """Hook called after app uninstallation"""
    print("👋 Barcode Generator uninstalled successfully!")
    print("💡 Note: Dependencies (reportlab, barcode, etc.) are still installed.")
