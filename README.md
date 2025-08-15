# Barcode Generator

A powerful Frappe app for generating bulk barcodes with customizable layouts, thermal label support, and automatic PDF generation.

## ✨ Features

- **Multiple Barcode Types**: Support for Code128, Code39, EAN13, EAN8, UPC-A, ITF, DataMatrix, and PDF417
- **Bulk Generation**: Generate hundreds of barcodes from a simple text input
- **Thermal Label Support**: Optimized for 50x25mm thermal printers (TA-P05 compatible)
- **Customizable Layout**: Configure codes per row, dimensions, and text inclusion
- **Multiple Page Sizes**: A4, Letter, A3, A5, Legal, and 50x25mm thermal labels
- **Item Name Support**: Display item names above barcodes with customizable fonts
- **Auto PDF Generation**: Generates organized PDF files ready for printing
- **Status Tracking**: Monitor generation progress and completion
- **Role-based Permissions**: System Manager, Barcode Manager, and Barcode User roles
- **Optimized Spacing**: Anti-overlap technology for perfect thermal printing

## 📦 Requirements

**Manual Installation Required** - Install these packages manually for better control:

```bash
pip install reportlab>=4.0.4 python-barcode>=0.15.1 Pillow>=10.2.0 qrcode>=7.4.2
```

## 🚀 Installation

### Recommended Method: Manual Dependencies

```bash
# Step 1: Install Python dependencies
pip install reportlab>=4.0.4 python-barcode>=0.15.1 Pillow>=10.2.0 qrcode>=7.4.2

# Step 2: Install the app
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/exvas/barcode_generator.git
bench install-app barcode_generator
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

### Standard Paper Printing (A4, Letter, etc.)

1. **Navigate to Barcode Generator**
   - Go to `Modules > Barcode Generator > Bulk Barcode Generator`

2. **Create a New Session**
   - Set a meaningful session name
   - Choose your barcode type (Code128 recommended)
   - Select page size (A4 for standard printing)

3. **Input Your Data**
   - Enter codes/numbers, one per line
   - Configure layout (codes per row: 3, dimensions)
   - Set font size for item names (24pt for A4)

4. **Generate PDF**
   - Click "Save" to process
   - Download the generated PDF from the "Generated PDF" field

### Thermal Label Printing (50x25mm)

1. **Select Thermal Format**
   - Page Size: `50x25mm Label`
   - Barcode Width: `38 mm`
   - Barcode Height: `8 mm`
   - Font Size: `12 pt`

2. **Input Data with Item Names**
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

### Layout Configuration
- **Codes Per Row**: Default 3 (A4), 1 (thermal)
- **Include Text**: Show/hide code text below barcodes
- **Font Size**: 
  - A4 Paper: 18-28pt for item names
  - Thermal Labels: 10-14pt for item names

### Dimensions

#### Standard Paper (A4, Letter, etc.)
- **Width**: 37-50mm (optimized for A4)
- **Height**: 15-18mm (including text space)

#### Thermal Labels (50x25mm)
- **Width**: 38-42mm (fits with margins)
- **Height**: 8-10mm (leaves space for text)

## 🛠️ API Usage

Generate barcodes programmatically:

```python
import frappe

# Standard A4 barcodes
doc = frappe.get_doc({
    "doctype": "Bulk Barcode Generator",
    "title": "A4 Barcode Session",
    "input_data": "Product A,12345\nProduct B,67890",
    "barcode_type": "Code128",
    "page_size": "A4",
    "codes_per_row": 3,
    "barcode_width": 50,
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
doc.generate_pdf()

# Get the generated PDF
pdf_url = doc.generated_pdf
```

## 🔐 Permissions

The app includes three permission levels:

- **System Manager**: Full access (create, read, write, delete)
- **Barcode Manager**: Full access (create, read, write, delete)  
- **Barcode User**: Limited access (create, read, write, no delete)

## 🔧 Troubleshooting

### Common Issues

1. **Import Error: No module named 'reportlab'**
   - Install dependencies manually for better control:
   ```bash
   pip install reportlab>=4.0.4 python-barcode>=0.15.1 Pillow>=10.2.0 qrcode>=7.4.2
   ```

2. **PDF Generation Failed**
   - Check that input data contains valid codes
   - Ensure barcode type matches your data format
   - Verify sufficient disk space for PDF generation

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
| Poor print quality | Adjust printer darkness/speed settings |

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

### A4 Paper Labels
```
Input: Product A,12345
Settings: A4, 50mm x 15mm, 24pt font
Result: Professional A4 labels with large text
```

### Thermal Labels (TA-P05)
```
Input: 1/2 ELBOW CPVC,0010251279
Settings: 50x25mm Label, 38mm x 8mm, 12pt font
Result: Perfect thermal labels for TA-P05 printer
```
