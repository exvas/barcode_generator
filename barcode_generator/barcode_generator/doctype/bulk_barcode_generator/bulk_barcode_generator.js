// File: apps/barcode_generator/barcode_generator/doctype/bulk_barcode_generator/bulk_barcode_generator.js

frappe.ui.form.on('Bulk Barcode Generator', {
    refresh: function(frm) {
        // Add custom buttons
        frm.add_custom_button(__('Generate PDF'), function() {
            generate_barcode_pdf(frm);
        }, __('Actions'));
        
        frm.add_custom_button(__('Preview Codes'), function() {
            preview_input_codes(frm);
        }, __('Actions'));
        
        // Add download button if PDF exists
        if (frm.doc.generated_pdf) {
            frm.add_custom_button(__('Download PDF'), function() {
                window.open(frm.doc.generated_pdf, '_blank');
            }, __('Actions'));
        }
        
        // Set default values
        if (frm.is_new()) {
            frm.set_value('barcode_type', 'Code128');
            frm.set_value('page_size', 'A4');
            frm.set_value('codes_per_row', 3);
            frm.set_value('include_text', 1);
            frm.set_value('barcode_width', 50);
            frm.set_value('barcode_height', 15);
        }
        
        // Update total codes when input changes
        update_code_count(frm);
    },
    
    download_template: function(frm) {
        // Handle template download
        window.open('/api/method/barcode_generator.barcode_generator.doctype.bulk_barcode_generator.bulk_barcode_generator.download_template', '_blank');
    },
    
    upload_file: function(frm) {
        // When file is uploaded, process it
        if (frm.doc.upload_file) {
            frm.save().then(() => {
                frm.reload_doc();
                frappe.show_alert({
                    message: __('File processed successfully!'),
                    indicator: 'green'
                });
            });
        }
    },
    
    input_data: function(frm) {
        // Update code count when input data changes
        update_code_count(frm);
    },
    
    barcode_type: function(frm) {
        // Show/hide dimensions based on barcode type
        if (['DataMatrix', 'PDF417'].includes(frm.doc.barcode_type)) {
            frm.set_df_property('barcode_width', 'hidden', 0);
            frm.set_df_property('barcode_height', 'hidden', 0);
        }
    }
});

function update_code_count(frm) {
    if (frm.doc.input_data) {
        let codes = frm.doc.input_data.split('\n').filter(line => line.trim());
        frm.set_value('total_codes', codes.length);
        
        // Show warning for large batches
        if (codes.length > 500) {
            frm.dashboard.add_comment(__('Large batch detected. Processing may take several minutes.'), 'orange');
        }
    }
}

function preview_input_codes(frm) {
    let data_source = "";
    
    if (frm.doc.upload_file && frm.doc.input_data) {
        data_source = "from uploaded file";
    } else if (frm.doc.input_data) {
        data_source = "from manual input";
    }
    
    if (!frm.doc.input_data) {
        frappe.msgprint(__('Please upload a file or enter some codes manually first'));
        return;
    }
    
    frappe.call({
        method: 'barcode_generator.barcode_generator.doctype.bulk_barcode_generator.bulk_barcode_generator.preview_codes',
        args: {
            input_data: frm.doc.input_data
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                let codes = r.message.codes;
                let total = r.message.total_count;
                let has_more = r.message.has_more;
                let format_info = r.message.format_info || "";
                
                let html = `
                    <div style="max-height: 400px; overflow-y: auto;">
                        <h4>Preview (First 10 codes) ${data_source}</h4>
                        <p><strong>Total codes found: ${total}</strong></p>
                        ${format_info ? `<p><em>${format_info}</em></p>` : ''}
                        <ol>
                `;
                
                codes.forEach(code => {
                    html += `<li><code>${code}</code></li>`;
                });
                
                html += '</ol>';
                
                if (has_more) {
                    html += `<p><em>... and ${total - 10} more codes</em></p>`;
                }
                
                html += '</div>';
                
                let dialog = new frappe.ui.Dialog({
                    title: __('Code Preview'),
                    fields: [
                        {
                            fieldtype: 'HTML',
                            fieldname: 'preview_html',
                            options: html
                        }
                    ]
                });
                dialog.show();
            } else {
                frappe.msgprint(__('Error previewing codes: ') + (r.message?.message || 'Unknown error'));
            }
        }
    });
}

function generate_barcode_pdf(frm) {
    // Validate form
    if (!frm.doc.input_data) {
        frappe.msgprint(__('Please enter codes to generate barcodes'));
        return;
    }
    
    if (!frm.doc.name) {
        frappe.msgprint(__('Please save the document first'));
        return;
    }
    
    // Show confirmation dialog
    let total_codes = frm.doc.total_codes || 0;
    frappe.confirm(
        __(`Generate PDF with ${total_codes} barcodes?<br><br>
           This may take a few minutes for large batches.`),
        function() {
            // Start generation
            frappe.show_progress(__('Generating Barcodes'), 0, 100, __('Starting...'));
            
            frappe.call({
                method: 'barcode_generator.barcode_generator.doctype.bulk_barcode_generator.bulk_barcode_generator.generate_pdf',
                args: {
                    doc_name: frm.doc.name
                },
                callback: function(r) {
                    frappe.hide_progress();
                    
                    if (r.message && r.message.success) {
                        frm.reload_doc();
                        frappe.show_alert({
                            message: __('PDF generated successfully!'),
                            indicator: 'green'
                        });
                        
                        // Automatically download
                        if (r.message.file_url) {
                            setTimeout(() => {
                                window.open(r.message.file_url, '_blank');
                            }, 1000);
                        }
                    } else {
                        frappe.msgprint({
                            title: __('Generation Failed'),
                            message: r.message?.message || __('Unknown error occurred'),
                            indicator: 'red'
                        });
                    }
                },
                error: function(r) {
                    frappe.hide_progress();
                    frappe.msgprint({
                        title: __('Error'),
                        message: __('Failed to generate PDF. Please try again.'),
                        indicator: 'red'
                    });
                }
            });
        }
    );
}

// Real-time progress updates
frappe.realtime.on('progress', function(data) {
    if (data.title && data.title.includes('barcode')) {
        frappe.show_progress(data.title, data.percent, 100, data.description);
    }
});