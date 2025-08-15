#!/usr/bin/env python3

import frappe

def test_thermal_barcodes():
    """Test thermal barcode generation"""
    
    print("=== Thermal Barcode Generation Test ===")
    
    # Create test document
    doc = frappe.get_doc({
        'doctype': 'Bulk Barcode Generator',
        'title': 'Thermal Test Console',
        'input_data': 'Test1,111111\nTest2,222222\nTest3,333333',
        'barcode_type': 'Code128',
        'page_size': '50x25mm Label',
        'barcode_width': 38,
        'barcode_height': 8,
        'item_name_font_size': 12,
        'include_text': 1
    })
    
    print("✅ Creating test document...")
    doc.insert()
    print(f"✅ Document created: {doc.name}")
    
    print("✅ Parsing input data...")
    codes = doc.parse_input_data()
    print(f"✅ Parsed codes: {codes}")
    print(f"✅ Total codes: {len(codes)}")
    
    # Test page size
    page_size = doc.get_page_size()
    print(f"✅ Page size: {page_size}")
    
    print("✅ Testing barcode generation...")
    try:
        # Generate barcode images first
        barcode_images = []
        for item_name, barcode_num in codes:
            print(f"  - Generating: {item_name} -> {barcode_num}")
            img = doc.generate_barcode_image(barcode_num, item_name)
            if img:
                barcode_images.append((item_name, barcode_num, img))
        
        print(f"✅ Generated {len(barcode_images)} barcode images")
        
        # Test PDF generation
        doc.generate_pdf()
        print("✅ PDF generation completed successfully!")
        print(f"✅ Generated PDF: {doc.generated_pdf}")
        
        return doc
        
    except Exception as e:
        print(f"❌ Error during generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_thermal_barcodes()
