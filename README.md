# Barcode Generator

A powerful Frappe app for generating bulk barcodes with customizable layouts and automatic PDF generation.

## Features

- **Multiple Barcode Types**: Support for Code128, Code39, EAN13, EAN8, UPC-A, ITF, DataMatrix, and PDF417
- **Bulk Generation**: Generate hundreds of barcodes from a simple text input
- **Customizable Layout**: Configure codes per row, dimensions, and text inclusion
- **Multiple Page Sizes**: A4, Letter, A3, A5, and Legal page formats
- **Auto PDF Generation**: Generates organized PDF files ready for printing
- **Status Tracking**: Monitor generation progress and completion
- **Role-based Permissions**: System Manager, Barcode Manager, and Barcode User roles

## Requirements

The following Python packages are automatically installed when you install the app:

- `reportlab>=4.0.4` - PDF generation
- `python-barcode>=0.15.1` - Barcode generation
- `Pillow>=10.2.0` - Image processing
- `qrcode>=7.4.2` - QR code support

## Installation

### Method 1: Automatic Installation (Recommended)

The app includes automatic dependency validation and installation:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/exvas/barcode_generator.git
bench install-app barcode_generator
```

### Method 2: Manual Installation with Script

For manual dependency management, use the included installation script:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/exvas/barcode_generator.git

# Run the installation script
bash apps/barcode_generator/barcode_generator/install_barcode_app.sh your-site-name
```

## Usage

1. **Navigate to Barcode Generator**
   - Go to `Modules > Barcode Generator > Bulk Barcode Generator`

2. **Create a New Session**
   - Set a meaningful session name
   - Choose your barcode type (Code128 recommended)
   - Select page size (A4 default)

3. **Input Your Data**
   - Enter codes/numbers, one per line
   - Configure layout (codes per row, dimensions)
   - Set font size for item names

4. **Generate PDF**
   - Click "Save" to process
   - Download the generated PDF from the "Generated PDF" field

## Configuration Options

### Barcode Settings
- **Type**: Code128, Code39, EAN13, EAN8, UPC-A, ITF, DataMatrix, PDF417
- **Page Size**: A4, Letter, A3, A5, Legal

### Layout Configuration
- **Codes Per Row**: Default 3 (adjustable)
- **Include Text**: Show/hide code text below barcodes
- **Font Size**: 8-16pt for item names

### Dimensions
- **Width**: Default 37mm (standard Code128)
- **Height**: Default 18mm (including text space)

## API Usage

Generate barcodes programmatically:

```python
import frappe

# Create a new barcode generation session
doc = frappe.get_doc({
    "doctype": "Bulk Barcode Generator",
    "title": "My Barcode Session",
    "input_data": "12345\n67890\n11111",
    "barcode_type": "Code128",
    "page_size": "A4",
    "codes_per_row": 3
})
doc.insert()
doc.generate_pdf()

# Get the generated PDF
pdf_url = doc.generated_pdf
```

## Permissions

The app includes three permission levels:

- **System Manager**: Full access (create, read, write, delete)
- **Barcode Manager**: Full access (create, read, write, delete)  
- **Barcode User**: Limited access (create, read, write, no delete)

## Troubleshooting

### Common Issues

1. **Import Error: No module named 'reportlab'**
   - The app automatically installs dependencies, but if you encounter this error, manually install:
   ```bash
   pip install reportlab>=4.0.4 python-barcode>=0.15.1 Pillow>=10.2.0 qrcode>=7.4.2
   ```

2. **PDF Generation Failed**
   - Check that input data contains valid codes
   - Ensure barcode type matches your data format
   - Verify sufficient disk space for PDF generation

3. **Permission Denied**
   - Ensure you have the correct role assigned
   - Contact your system administrator for access

## Development

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

## License

MIT License - see [license.txt](license.txt) for details.

## Support

For issues and questions:
- Create an issue on [GitHub](https://github.com/exvas/barcode_generator/issues)
- Contact: sammish.thundiyil@gmail.com
