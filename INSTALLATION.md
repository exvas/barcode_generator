# Barcode Generator App - Installation Guide

## Quick Installation

The Barcode Generator app now includes automatic dependency installation. Simply run:

```bash
# Install on a specific site
bench --site [site-name] install-app barcode_generator

# Example
bench --site petro install-app barcode_generator
```

## What Happens During Installation

1. **Before Installation Hook**: The app automatically installs required Python packages:
   - `reportlab>=4.0.4` - For PDF generation
   - `python-barcode>=0.15.1` - For barcode generation
   - `Pillow>=10.2.0` - For image processing
   - `qrcode>=7.4.2` - For QR code generation

2. **App Installation**: The app DocTypes and files are installed

3. **After Installation Hook**: Verification and cleanup

## Manual Dependency Installation (if needed)

If automatic installation fails, you can manually install dependencies:

```bash
# From bench directory
./env/bin/pip install reportlab>=4.0.4 python-barcode>=0.15.1 Pillow>=10.2.0 qrcode>=7.4.2

# Or install from requirements.txt
./env/bin/pip install -r apps/barcode_generator/requirements.txt
```

## Verification

After installation, verify the app is working:

1. Go to your ERPNext site
2. Search for "Bulk Barcode Generator" in the awesome bar
3. Create a new barcode generation session
4. Test PDF generation

## Features

✅ **A4 Paper Optimized**: Large fonts (24pt) and barcode sizes (50×25mm)  
✅ **Professional Layout**: Optimized spacing and positioning  
✅ **Automatic Dependencies**: No manual package installation required  
✅ **Multiple Formats**: Supports various barcode types  
✅ **Bulk Generation**: Generate multiple barcodes in one PDF  

## Troubleshooting

If you encounter import errors during installation:

1. Ensure you have Python 3.8+ 
2. Check virtual environment is active
3. Try manual dependency installation (see above)
4. Re-run the app installation

## Sites with Barcode Generator Installed

Currently installed on:
- `ai` site
- `extra.com` site  
- `petro` site

## Support

For issues or questions, check the error logs:
```bash
bench --site [site-name] logs
```
