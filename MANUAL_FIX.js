// Manual Fix Script
// Copy and paste this into your browser's Developer Console (F12)

// Clear the form cache and force reload the DocType meta
frappe.model.clear_doc("DocType", "Bulk Barcode Generator");

// Get fresh meta from server
frappe.call({
    method: "frappe.desk.form.load.getdoc",
    args: {
        doctype: "DocType",
        name: "Bulk Barcode Generator"
    },
    callback: function(r) {
        if (r.message) {
            // Clear the meta cache
            delete frappe.meta.docfield_map["Bulk Barcode Generator"];
            delete frappe.meta.doctypes["Bulk Barcode Generator"];
            
            // Force reload the page
            location.reload();
        }
    }
});

// Alternative: Directly update the field options in the browser
setTimeout(function() {
    if (cur_frm && cur_frm.doctype === "Bulk Barcode Generator") {
        var field = cur_frm.get_field("page_size");
        if (field) {
            field.df.options = "A4\nLetter\nA3\nA5\nLegal\n50x25mm Label";
            field.df.description = "Choose 50x25mm Label for thermal label printers";
            field.refresh();
        }
    }
}, 1000);
