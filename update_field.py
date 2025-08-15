#!/usr/bin/env python3

import frappe

def update_page_size_field():
    """Update the page_size field options to include 50x25mm Label"""
    
    # Connect to the site
    import os
    os.chdir('/Users/sammishthundiyil/frappe-bench-extra')
    frappe.init(site='petro')
    frappe.connect()
    
    try:
        # Get the DocField for page_size
        docfield = frappe.get_doc("DocField", {
            "parent": "Bulk Barcode Generator",
            "fieldname": "page_size"
        })
        
        # Update the options
        new_options = "A4\nLetter\nA3\nA5\nLegal\n50x25mm Label"
        docfield.options = new_options
        docfield.description = "Choose 50x25mm Label for thermal label printers"
        
        # Save the changes
        docfield.save()
        frappe.db.commit()
        
        print("✅ Successfully updated page_size field options")
        print(f"New options: {new_options}")
        
        # Clear cache
        frappe.clear_cache(doctype="Bulk Barcode Generator")
        print("✅ Cache cleared")
        
    except Exception as e:
        print(f"❌ Error updating field: {e}")
        frappe.db.rollback()
    
    finally:
        frappe.destroy()

if __name__ == "__main__":
    update_page_size_field()
