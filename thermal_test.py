#!/usr/bin/env python3
import frappe
import os

def test_thermal_generation():
    print("Starting thermal barcode test...")
    
    # Create a test document
    doc = frappe.get_doc({
        'doctype': 'Bulk Barcode Generator',
        'title': 'Thermal Test',
        'input_data': 'Item1,111111\nItem2,222222\nItem3,333333',
        'barcode_type': 'Code128',
        'page_size': '50x25mm Label',
        'barcode_width': 38,
        'barcode_height': 8,
        'item_name_font_size': 12,
        'include_text': 1
    })
    
    print(f"Document created with page_size: {doc.page_size}")
    doc.insert()
    print(f"Document saved as: {doc.name}")
    
    # Parse input data
    codes = doc.parse_input_data()
    print(f"Parsed {len(codes)} codes: {codes}")
    
    # Get page size
    page_size = doc.get_page_size()
    print(f"Page dimensions: {page_size}")
    
    # Check thermal label logic
    is_thermal = doc.page_size == '50x25mm Label'
    print(f"Is thermal label: {is_thermal}")
    
    if is_thermal:
        print("Using thermal label settings")
    else:
        print("Using standard paper settings")
    
    # Generate PDF
    try:
        doc.generate_pdf()
        print("✅ PDF generation successful!")
        print(f"Generated PDF: {doc.generated_pdf}")
        
        # Check if file exists
        if doc.generated_pdf:
            file_path = frappe.get_site_path() + doc.generated_pdf
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"PDF file size: {file_size} bytes")
                print(f"File path: {file_path}")
            else:
                print("❌ PDF file not found on disk")
        
    except Exception as e:
        print(f"❌ Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_thermal_generation()
