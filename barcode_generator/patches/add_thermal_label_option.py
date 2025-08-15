import frappe

def execute():
    """Add 50x25mm Label option to page_size field"""
    try:
        # Update the DocField directly using SQL to avoid parsing issues
        frappe.db.sql("""
            UPDATE `tabDocField` 
            SET `options` = 'A4\nLetter\nA3\nA5\nLegal\n50x25mm Label',
                `description` = 'Choose 50x25mm Label for thermal label printers'
            WHERE `parent` = 'Bulk Barcode Generator' 
            AND `fieldname` = 'page_size'
        """)
        
        frappe.db.commit()
        
        # Clear cache for the DocType
        frappe.clear_cache(doctype="Bulk Barcode Generator")
        
        print("✅ Successfully added 50x25mm Label option to page_size field")
        
    except Exception as e:
        print(f"❌ Error updating field: {e}")
        frappe.db.rollback()
        raise
