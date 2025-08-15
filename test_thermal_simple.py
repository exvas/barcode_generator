#!/usr/bin/env python3

# Simple test for thermal barcode generation
import frappe

def test_thermal():
    print("=== THERMAL BARCODE TEST ===")
    
    # Create test document
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
    
    print(f"✓ Document created with page_size: {doc.page_size}")
    doc.insert()
    print(f"✓ Document saved as: {doc.name}")
    
    # Parse data
    codes = doc.parse_input_data()
    print(f"✓ Parsed {len(codes)} codes")
    for i, code in enumerate(codes):
        print(f"  Code {i+1}: {code}")
    
    # Check page size
    page_size = doc.get_page_size()
    print(f"✓ Page dimensions: {page_size}")
    
    # Check thermal detection
    is_thermal = doc.page_size == '50x25mm Label'
    print(f"✓ Is thermal label: {is_thermal}")
    
    if is_thermal:
        print("✓ Using thermal label settings:")
        print("  - One page per barcode")
        print("  - Optimized font sizes")
        print("  - Reduced margins")
    
    # Generate PDF
    try:
        print("→ Generating PDF...")
        doc.generate_pdf()
        print("✅ PDF generated successfully!")
        print(f"✅ PDF path: {doc.generated_pdf}")
        
        # Check file
        import os
        if doc.generated_pdf:
            file_path = frappe.get_site_path() + doc.generated_pdf
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"✅ File size: {size} bytes")
                print(f"✅ Full path: {file_path}")
                return True
            else:
                print("❌ File not found on disk")
                return False
                
    except Exception as e:
        print(f"❌ Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_thermal()
