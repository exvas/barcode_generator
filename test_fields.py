#!/usr/bin/env python3
"""
Test if the new fields are accessible
"""
import sys
import os

# Add frappe to the path
sys.path.insert(0, "/Users/sammishthundiyil/frappe-bench-extra/apps/frappe")

try:
    import frappe
    import json
    
    # Load the DocType JSON to verify our changes
    doctype_path = "/Users/sammishthundiyil/frappe-bench-extra/apps/barcode_generator/barcode_generator/barcode_generator/doctype/bulk_barcode_generator/bulk_barcode_generator.json"
    
    with open(doctype_path, 'r') as f:
        doctype_json = json.load(f)
    
    print("=== Checking DocType Fields ===")
    
    # Check if our new fields exist in the JSON
    field_names = [field.get('fieldname') for field in doctype_json.get('fields', [])]
    
    new_fields = ['upload_file', 'download_template']
    
    for field in new_fields:
        if field in field_names:
            print(f"✅ {field} field found in DocType JSON")
        else:
            print(f"❌ {field} field NOT found in DocType JSON")
    
    print(f"\nTotal fields in DocType: {len(field_names)}")
    print("Field list:", field_names)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
