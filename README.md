# Barcode Generator

A powerful Frappe app for generating bulk barcodes with customizable layouts, thermal label support, and **optimized spacing for maximum density** on standard paper sizes.

## ✨ Features

- **Multiple Barcode Types**: Support for Code128, Code39, EAN13, EAN8, UPC-A, ITF, DataMatrix, and PDF417
- **Bulk Generation**: Generate hundreds of barcodes from text input or file uploads
- **File Upload Support**: Upload CSV/Excel files with automatic data processing
- **Template Download**: Get sample CSV templates for easy data formatting
- **Thermal Label Support**: Optimized for 50x25mm thermal printers (TA-P05 compatible)
- **High-Density Layouts**: **Optimized spacing for A4, A5, Letter, Legal** - fit maximum 5+ rows per page
- **Customizable Layout**: Configure codes per row, dimensions, and text inclusion
- **Multiple Page Sizes**: A4, Letter, A3, A5, Legal, and 50x25mm thermal labels
- **Item Name Support**: Display item names above barcodes with customizable fonts
- **Smart Preview**: Enhanced preview with intelligent format detection
- **Auto PDF Generation**: Generates organized PDF files ready for printing
- **Status Tracking**: Monitor generation progress and completion
- **Role-based Permissions**: System Manager, Barcode Manager, and Barcode User roles
- **Anti-Overlap Technology**: Perfect spacing for both thermal and standard printing

## 📦 Requirements

**✅ AUTOMATIC INSTALLATION AVAILABLE** - Dependencies are now installed automatically!

**Dependencies (Installed Automatically):**

**Core Barcode Libraries:**
- reportlab>=4.0.4
- python-barcode>=0.15.1
- Pillow>=10.2.0
- qrcode>=7.4.2

**File Upload Support (CSV/Excel):**
- pandas>=1.3.0
- openpyxl>=3.0.0

## 🚀 Installation

### 🎯 Method 1: Automatic Installation (Recommended)

**One-command installation with auto dependency management:**

```bash
# Step 1: Get the app
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/exvas/barcode_generator.git

# Step 2: Run auto-installer
cd apps/barcode_generator
./install_barcode_generator.sh
```

**Or download and run directly:**
```bash
cd $PATH_TO_YOUR_BENCH
wget https://raw.githubusercontent.com/exvas/barcode_generator/main/install_barcode_generator.sh
chmod +x install_barcode_generator.sh
./install_barcode_generator.sh
```

### 🔧 Method 2: Manual Installation

```bash
# Step 1: Get the app
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/exvas/barcode_generator.git

# Step 2: Install dependencies (automatically installed when you install the app)
bench --site YOUR_SITE_NAME install-app barcode_generator

# Step 3: Dependencies are installed automatically via hooks!
# That's it! The app will install all required packages during installation.
```

### 🛠️ Method 3: Manual Dependencies (Advanced Users)

If you prefer to manage dependencies manually:

```bash
# Install dependencies first
pip install reportlab>=4.0.4 python-barcode>=0.15.1 Pillow>=10.2.0 qrcode>=7.4.2 pandas>=1.3.0 openpyxl>=3.0.0

# Then install the app
bench --site YOUR_SITE_NAME install-app barcode_generator
```

## 🏷️ Thermal Label Printing

### Supported Thermal Printers
- **TA-P05** (tested and optimized)
- **50x25mm label format**
- Other thermal printers supporting 50x25mm labels

### Optimal Thermal Settings

| Setting | Recommended Value | Purpose |
|---------|------------------|---------|
| **Page Size** | `50x25mm Label` | Thermal label format |
| **Barcode Width** | `38-42 mm` | Fits within 50mm with margins |
| **Barcode Height** | `8-10 mm` | Leaves space for text |
| **Item Name Font Size** | `12-14 pt` | Readable on thermal labels |
| **Include Text Below Barcode** | ✅ Enabled | Shows barcode numbers |

### Thermal Input Data Format

```
Item Name,Barcode Number
Product A,0010251279
1/2 ELBOW CPVC,0010251280
TEE JOINT,0010251281
COUPLING,0010251282
```

## 📝 Usage

### Upload CSV/Excel Files (Recommended)

**Perfect for bulk barcode generation with organized data!**

1. **Navigate to Barcode Generator**
   - Go to `Modules > Barcode Generator > Bulk Barcode Generator`

2. **Download Template** 
   - Click "Download Template" to get the sample CSV format
   - Template includes proper headers: "Item Name", "Barcode Number"

3. **Prepare Your Data**
   - Fill the CSV with your items following the format:
   ```csv
   Item Name,Barcode Number
   1/2 PIPE CPVC NIPRO,01192202500024
   3/4 ELBOW CPVC,01192202500025
   TEE JOINT CPVC,01192202500026
   ```

4. **Upload and Generate**
   - Upload your CSV/Excel file using "Upload CSV/Excel File"
   - Choose your barcode settings (Code128, page size, etc.)
   - Click "Preview Codes" to verify data
   - Click "Generate PDF" to create your barcodes

### Manual Input (Alternative)

**For quick barcode generation without files:**

### Standard Paper Printing (A4, A5, Letter, Legal) - **OPTIMIZED**

**Perfect for high-density barcode printing - Maximum 5+ rows per page!**

1. **Create a New Session**
   - Set a meaningful session name
   - Choose your barcode type (Code128 recommended)
   - Select page size (A4, A5, Letter, or Legal)

2. **Input Your Data** (Choose one method)
   - **Upload File**: Use CSV/Excel with "Item Name,Barcode Number" format
   - **Manual Entry**: Enter codes directly with supported formats:
     - `Item Name,Barcode Number` (CSV format)
     - `Item Name | Barcode Number` (Pipe separated)
     - `Item Name  Barcode Number` (Space separated)
     - `Barcode Number` (Just barcode)

3. **Configure Layout**
   - Codes per row: 3 recommended for optimal density
   - Font size: 24pt optimized for readability
   - Include text below barcode: ✅ Enabled

4. **Generate PDF**
   - Click "Preview Codes" to verify format
   - Click "Generate PDF" to create barcodes
   - Download the generated PDF

**🎯 A4/Letter Optimization Results:**
- **Reduced margins**: 15mm instead of 20mm for more space
- **Minimal row spacing**: Only 5mm between barcode rows  
- **Compact dimensions**: 35mm x 15mm barcodes for perfect density
- **Maximum barcodes**: 5+ rows easily fit on one page

### Thermal Label Printing (50x25mm)

1. **Select Thermal Format**
   - Page Size: `50x25mm Label`
   - Barcode Width: `38 mm`
   - Barcode Height: `8 mm`
   - Font Size: `12 pt`

2. **Input Data with Item Names**
   
   **Option 1: Upload CSV/Excel File**
   - Download template and fill with your data
   - Upload using "Upload CSV/Excel File" field
   
   **Option 2: Manual Entry**
   ```
   Product A,0010251279
   Product B,0010251280
   1/2 ELBOW CPVC,0010251281
   ```

3. **Print Settings for TA-P05**
   - Paper Size: 50mm x 25mm labels
   - Print Quality: High/Best
   - Print Speed: Medium
   - Darkness: Medium-High

## ⚙️ Configuration Options

### Barcode Settings
- **Type**: Code128, Code39, EAN13, EAN8, UPC-A, ITF, DataMatrix, PDF417
- **Page Size**: A4, Letter, A3, A5, Legal, **50x25mm Label**

### Layout Configuration - **OPTIMIZED FOR DENSITY**

#### Standard Papers (A4, A5, Letter, Legal)
- **Codes Per Row**: Default 3 (optimal spacing)
- **Margins**: 15mm (reduced for maximum space)
- **Row Spacing**: 5mm minimal gap between rows
- **Maximum Rows**: 5+ rows per page easily achievable

#### Thermal Labels (50x25mm)  
- **Codes Per Row**: 1 (one barcode per label)
- **Perfect consecutive printing** (no skipping)

### Font Sizes
- **Standard Paper**: 18-28pt for item names
- **Thermal Labels**: 10-14pt for item names

### Dimensions - **NEW OPTIMIZED SIZES**

#### Standard Paper (A4, A5, Letter, Legal) - **MAXIMUM DENSITY**
- **Width**: 35mm (optimized for 3-per-row layout)
- **Height**: 15mm (includes text space, minimized gap)
- **Total Item Height**: ~20mm (barcode + text + minimal padding)
- **Result**: **5+ rows per A4 page** instead of 3-4 rows

#### Thermal Labels (50x25mm) - **UNCHANGED (PERFECT)**
- **Width**: 38-42mm (fits with margins)
- **Height**: 8-10mm (leaves space for text)
- **One barcode per thermal label** (consecutive printing)

## 🛠️ API Usage

Generate barcodes programmatically:

```python
import frappe

# Upload CSV file method (Recommended)
doc = frappe.get_doc({
    "doctype": "Bulk Barcode Generator",
    "title": "CSV Upload Session",
    "upload_file": "/files/my_barcode_data.csv",  # Path to uploaded CSV
    "barcode_type": "Code128",
    "page_size": "A4",
    "codes_per_row": 3,
    "barcode_width": 35,
    "barcode_height": 15,
    "item_name_font_size": 24
})

# Manual input method  
doc = frappe.get_doc({
    "doctype": "Bulk Barcode Generator",
    "title": "A4 High-Density Session",
    "input_data": "Product A,12345\nProduct B,67890\nProduct C,11111",
    "barcode_type": "Code128",
    "page_size": "A4",
    "codes_per_row": 3,
    "barcode_width": 35,
    "barcode_height": 15,  
    "item_name_font_size": 24
})

# Thermal label barcodes
thermal_doc = frappe.get_doc({
    "doctype": "Bulk Barcode Generator", 
    "title": "Thermal Label Session",
    "input_data": "1/2 ELBOW CPVC,0010251279\nTEE JOINT,0010251280",
    "barcode_type": "Code128",
    "page_size": "50x25mm Label",
    "barcode_width": 38,
    "barcode_height": 8,
    "item_name_font_size": 12,
    "include_text": 1
})

doc.insert()
doc.save()  # This processes uploaded file if provided

# Generate PDF
pdf_url = doc.create_pdf()
```

## 🔐 Permissions

The app includes three permission levels:

- **System Manager**: Full access (create, read, write, delete)
- **Barcode Manager**: Full access (create, read, write, delete)  
- **Barcode User**: Limited access (create, read, write, no delete)

## 🔧 Troubleshooting

### Common Issues

1. **Installation Dependencies**
   - ✅ **NEW**: Dependencies are installed automatically when you install the app!
   - If automatic installation fails, you'll see clear error messages
   - Fallback: Manual installation with provided commands

2. **Import Error: No module named 'reportlab'**
   - With auto-installation: This should not happen anymore
   - Manual fix: 
   ```bash
   pip install reportlab>=4.0.4 python-barcode>=0.15.1 Pillow>=10.2.0 qrcode>=7.4.2 pandas>=1.3.0 openpyxl>=3.0.0
   ```

3. **Automatic Installation Failed**
   - Check the installation logs for specific error messages
   - Ensure your bench environment has internet access
   - Try the manual installation method as fallback
   - Run: `bench --site YOUR_SITE install-app barcode_generator --verbose` for detailed logs

4. **File Upload Not Working**
   - Auto-installation includes pandas and openpyxl
   - If still not working, manually install: `pip install pandas>=1.3.0 openpyxl>=3.0.0`
   - Check file format: Use CSV or Excel (.xlsx, .xls)
   - Verify file has proper headers: "Item Name", "Barcode Number"

5. **AttributeError: object has no attribute 'upload_file'**
   - Run database migration: `bench --site YOUR_SITE migrate`
   - Clear cache: `bench --site YOUR_SITE clear-cache`
   - Restart bench: `bench restart`

4. **PDF Generation Failed**
   - Check that input data contains valid codes
   - Ensure barcode type matches your data format
   - Verify sufficient disk space for PDF generation

5. **Template Download Issues**
   - Check if download_template API method is accessible
   - Verify proper permissions for file downloads
   - Try manual CSV creation if download fails

3. **Thermal Label Issues**
   - Use format: `ItemName,BarcodeNumber`
   - Check Page Size is set to "50x25mm Label"
   - Verify barcode dimensions fit within 50x25mm
   - Test with recommended settings first

4. **Barcode Number Overlap**
   - Reduce barcode height (8-10mm for thermal)
   - Increase font spacing in settings
   - Check "Include Text Below Barcode" option

5. **Permission Denied**
   - Ensure you have the correct role assigned
   - Contact your system administrator for access

### Thermal Printer Troubleshooting

| Issue | Solution |
|-------|----------|
| Labels too big | Reduce width to 38mm, height to 8mm |
| Text unreadable | Increase font size to 14pt |
| Numbers overlap bars | Use latest version (overlap fixed) |
| Poor print quality |    - Adjust printer darkness/speed settings |

## 🚀 **NEW: Standard Paper Optimization**

### ⚡ Maximum Density Achieved

**Before vs After Optimization:**

| Paper Size | Before | After | Improvement |
|------------|--------|-------|-------------|
| **A4** | 3-4 rows | **5+ rows** | +25% more barcodes |
| **Letter** | 3-4 rows | **5+ rows** | +25% more barcodes |  
| **A5** | 2-3 rows | **4+ rows** | +33% more barcodes |
| **Legal** | 4-5 rows | **6+ rows** | +20% more barcodes |

### 🎯 Key Optimization Features

1. **Reduced Margins**: 15mm instead of 20mm (more printable area)
2. **Minimal Row Spacing**: Only 5mm between barcode rows
3. **Optimized Dimensions**: 35mm x 15mm perfect for readability and density
4. **Smart Font Sizing**: 24pt for excellent readability at reduced size
5. **Thermal Labels Unchanged**: 50x25mm labels work perfectly as before

### 💡 Best Practices for High Density

- **A4/Letter**: Use 3 codes per row for optimal balance
- **Font Size**: 24pt provides excellent readability at smaller dimensions  
- **Barcode Types**: Code128 and Code39 work best for high density
- **Testing**: Always test print one page before bulk printing

### 🔄 Migration Notice

- **Existing thermal label setups**: No changes needed, works perfectly
- **Standard paper users**: Automatic optimization, more barcodes per page
- **Custom dimensions**: Your settings will override optimized defaults

## 🏗️ Development

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/barcode_generator
pre-commit install
```

Pre-commit is configured to use the following tools:
- ruff
- eslint  
- prettier
- pyupgrade

### CI/CD

This app uses GitHub Actions for CI:
- **CI**: Installs app and runs unit tests on every push to `develop` branch
- **Linters**: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on pull requests

## 📄 License

MIT License - see [license.txt](license.txt) for details.

## 📞 Support

For issues and questions:
- Create an issue on [GitHub](https://github.com/exvas/barcode_generator/issues)
- Contact: sammish.thundiyil@gmail.com

---

## 🎯 Quick Start Examples

### CSV Upload Method (Recommended)
```csv
# Download template, fill with your data:
Item Name,Barcode Number
Product A,12345
Product B,67890
Product C,11111

# Upload file → Preview → Generate PDF
Settings: A4, 35mm x 15mm, 24pt font, 3 per row
Result: Professional barcodes with item names, 5+ rows per page
```

### Manual Entry Method
```
# Multiple format support:
Input: Product A,12345
       Product B | 67890  
       Product C  11111
       22222
Settings: A4, 35mm x 15mm, 24pt font, 3 per row
Result: Smart parsing, 5+ rows per page, minimal spacing
```

### A5/Letter Labels - **SPACE OPTIMIZED**  
```
# For smaller paper sizes:
Input: Upload CSV or manual entry
Settings: A5, 35mm x 15mm, 22pt font, 3 per row
Result: 4+ rows per page with professional appearance
```

### Thermal Labels (TA-P05) - **PERFECT FOR THERMAL PRINTING**
```csv
# Thermal-optimized format:
Item Name,Barcode Number
1/2 ELBOW CPVC,0010251279
TEE JOINT,0010251280

Settings: 50x25mm Label, 38mm x 8mm, 12pt font
Result: Perfect thermal labels, consecutive printing
```
