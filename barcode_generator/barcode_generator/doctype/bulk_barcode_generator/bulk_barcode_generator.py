# Enhanced version of bulk_barcode_generator.py to support item names

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_site_path
import os
import io
import base64
import csv
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter, A3, A5, legal
from reportlab.lib.units import mm
import qrcode
import re

# Try to import pandas, fall back to basic CSV handling if not available
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

class BulkBarcodeGenerator(Document):
    def validate(self):
        """Validate input data before saving"""
        # Process upload file if provided
        if self.upload_file and not self.input_data:
            self.process_uploaded_file()
        
        if not self.input_data:
            frappe.throw("Input data is required. Either upload a file or enter data manually.")
        
        # Count total codes
        codes = self.parse_input_data()
        self.total_codes = len(codes)
        
        if self.total_codes == 0:
            frappe.throw("No valid codes found in input data")
        
        if self.total_codes > 1000:
            frappe.throw("Maximum 1000 codes allowed per batch")

    def process_uploaded_file(self):
        """Process uploaded CSV/Excel file and populate input_data"""
        if not self.upload_file:
            return
        
        try:
            # Get the file
            file_doc = frappe.get_doc("File", {"file_url": self.upload_file})
            file_path = file_doc.get_full_path()
            
            # Read file based on extension
            if file_path.endswith('.csv'):
                if HAS_PANDAS:
                    df = pd.read_csv(file_path)
                    input_lines = self._process_dataframe(df)
                else:
                    # Fallback to basic CSV reading
                    input_lines = self._process_csv_basic(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                if HAS_PANDAS:
                    df = pd.read_excel(file_path)
                    input_lines = self._process_dataframe(df)
                else:
                    frappe.throw("Excel file support requires pandas. Please use CSV format or install pandas.")
            else:
                frappe.throw("Supported file formats: CSV, Excel (.xlsx, .xls)")
            
            # Set input_data
            self.input_data = "\n".join(input_lines)
            
            if not input_lines:
                frappe.throw("No valid data found in uploaded file")
                
        except Exception as e:
            frappe.throw(f"Error processing uploaded file: {str(e)}")

    def _process_dataframe(self, df):
        """Process pandas DataFrame and return input lines"""
        input_lines = []
        
        # Check if we have expected columns
        if len(df.columns) >= 2:
            # Use first two columns as Item Name and Barcode
            item_col = df.columns[0]
            barcode_col = df.columns[1]
            
            for _, row in df.iterrows():
                item_name = str(row[item_col]).strip() if pd.notna(row[item_col]) else ""
                barcode_num = str(row[barcode_col]).strip() if pd.notna(row[barcode_col]) else ""
                
                if barcode_num:  # Only add if barcode exists
                    if item_name:
                        input_lines.append(f"{item_name},{barcode_num}")
                    else:
                        input_lines.append(barcode_num)
        
        elif len(df.columns) == 1:
            # Single column - treat as barcode numbers only
            barcode_col = df.columns[0]
            for _, row in df.iterrows():
                barcode_num = str(row[barcode_col]).strip() if pd.notna(row[barcode_col]) else ""
                if barcode_num:
                    input_lines.append(barcode_num)
        
        else:
            frappe.throw("File must contain at least one column")
        
        return input_lines

    def _process_csv_basic(self, file_path):
        """Process CSV file using basic csv module"""
        input_lines = []
        
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:  # utf-8-sig to handle BOM
            # Try to detect delimiter
            sample = csvfile.read(1024)
            csvfile.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.reader(csvfile, delimiter=delimiter)
            
            # Skip header if it exists
            first_row = next(reader, None)
            if first_row and (first_row[0].lower().strip() in ['item', 'product', 'name', 'item name']):
                # Skip header row
                pass
            else:
                # Process first row as data
                if first_row:
                    csvfile.seek(0)
                    reader = csv.reader(csvfile, delimiter=delimiter)
            
            for row in reader:
                if not row:
                    continue
                    
                # Clean row data
                clean_row = [cell.strip() for cell in row if cell.strip()]
                
                if len(clean_row) >= 2:
                    # Two columns: Item Name, Barcode
                    item_name = clean_row[0]
                    barcode_num = clean_row[1]
                    if barcode_num:
                        input_lines.append(f"{item_name},{barcode_num}")
                elif len(clean_row) == 1:
                    # Single column: Just barcode
                    barcode_num = clean_row[0]
                    if barcode_num:
                        input_lines.append(barcode_num)
        
        return input_lines

    def parse_input_data(self):
        """Parse input data and return list of (item_name, barcode) tuples with improved handling"""
        if not self.input_data:
            return []
        
        codes = []
        for line in self.input_data.split('\n'):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
                
            # Try to parse different formats with improved logic:
            # Format 1: "Item Name,Barcode" or "Item Name\tBarcode"
            # Format 2: "Item Name | Barcode"  
            # Format 3: Just "Barcode" (no item name)
            # Format 4: "Item Name Barcode" (space separated)
            
            if ',' in line:
                # CSV format: Item Name,Barcode
                parts = line.split(',', 1)
                if len(parts) == 2:
                    item_name = parts[0].strip()
                    barcode_num = parts[1].strip()
                    codes.append((item_name, barcode_num))
                else:
                    # Just barcode with comma artifacts
                    clean_line = line.replace(',', '').strip()
                    if clean_line:
                        codes.append(("", clean_line))
                    
            elif '\t' in line:
                # Tab-separated: Item Name\tBarcode
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    item_name = parts[0].strip()
                    barcode_num = parts[1].strip()
                    codes.append((item_name, barcode_num))
                else:
                    clean_line = line.replace('\t', '').strip()
                    if clean_line:
                        codes.append(("", clean_line))
                    
            elif '|' in line:
                # Pipe-separated: Item Name | Barcode
                parts = line.split('|', 1)
                if len(parts) == 2:
                    item_name = parts[0].strip()
                    barcode_num = parts[1].strip()
                    codes.append((item_name, barcode_num))
                else:
                    clean_line = line.replace('|', '').strip()
                    if clean_line:
                        codes.append(("", clean_line))
            else:
                # Plain text - could be just barcode or "Item Name Barcode"
                clean_line = line.strip()
                if clean_line:
                    # Check if it contains multiple words and last word looks like a barcode
                    words = clean_line.split()
                    if len(words) >= 2:
                        # Check if last word looks like a barcode (alphanumeric, possibly with special chars)
                        last_word = words[-1]
                        if re.match(r'^[A-Za-z0-9\-_\.]+$', last_word) and len(last_word) >= 4:
                            # Treat last word as barcode, rest as item name
                            item_name = ' '.join(words[:-1])
                            barcode_num = last_word
                            codes.append((item_name, barcode_num))
                        else:
                            # Treat entire line as barcode
                            codes.append(("", clean_line))
                    else:
                        # Single word - treat as barcode number
                        codes.append(("", clean_line))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_codes = []
        for item_name, barcode_num in codes:
            key = f"{item_name}:{barcode_num}"
            if key not in seen:
                seen.add(key)
                unique_codes.append((item_name, barcode_num))
        
        return unique_codes

    def get_page_size(self):
        """Get page size in points"""
        page_sizes = {
            'A4': A4,
            'Letter': letter,
            'A3': A3,
            'A5': A5,
            'Legal': legal,
            '50x25mm Label': (50 * mm, 25 * mm)  # Thermal label size
        }
        return page_sizes.get(self.page_size, A4)

    def generate_barcode_image(self, code_text, item_name=""):
        """Generate a single barcode image with item name"""
        try:
            # Map barcode types
            barcode_classes = {
                'Code128': barcode.Code128,
                'Code39': barcode.Code39,
                'EAN13': barcode.EAN13,
                'EAN8': barcode.EAN8,
                'UPC-A': barcode.UPCA,
                'ITF': barcode.ITF,
            }
            
            if self.barcode_type in barcode_classes:
                # For standard barcodes
                barcode_class = barcode_classes[self.barcode_type]
                
                # Different options for thermal vs standard printing
                if self.page_size == '50x25mm Label':
                    # Thermal label optimized settings
                    options = {
                        'module_width': 0.25,   # Even smaller modules for thermal labels
                        'module_height': 6.0,   # Compact height for thermal
                        'quiet_zone': 1.5,     # Minimal quiet zone for thermal
                        'font_size': 8,         # Smaller font for thermal labels
                        'text_distance': 4.0,   # More space between bars and text to prevent overlap
                        'background': 'white',
                        'foreground': 'black',
                        'write_text': self.include_text,  # Control text display
                    }
                else:
                    # Standard paper optimized settings (A4, Letter, etc.)
                    options = {
                        'module_width': 0.5,    # Increased module width for A4 (0.5mm)
                        'module_height': 15.0,  # Increased height for better visibility
                        'quiet_zone': 6.0,      # Increased quiet zone for better scanning
                        'font_size': 18,        # Much larger font size for A4 readability
                        'text_distance': 8.0,   # More space between bars and text
                        'background': 'white',
                        'foreground': 'black',
                        'write_text': self.include_text,  # Control text display
                    }
                
                # Generate barcode
                code_obj = barcode_class(str(code_text), writer=ImageWriter())
                
                # Save to memory buffer
                buffer = io.BytesIO()
                code_obj.write(buffer, options=options)
                buffer.seek(0)
                
                # Open as PIL image and ensure it's RGB
                img = Image.open(buffer)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Add item name above the barcode if provided
                if item_name and item_name.strip():
                    img = self.add_item_name_to_image(img, item_name, code_text)
                
                return img
                
            elif self.barcode_type in ['DataMatrix', 'PDF417']:
                # For QR codes and 2D barcodes, use qrcode library
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(str(code_text))
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Add item name and barcode text
                if item_name and item_name.strip():
                    img = self.add_item_name_to_image(img, item_name, code_text)
                elif self.include_text:
                    img = self.add_text_to_image(img, code_text)
                
                return img
            
        except Exception as e:
            frappe.log_error(f"Error generating barcode for {code_text}: {str(e)}")
            # Return a placeholder image
            return self.create_error_image(code_text, str(e))

    def add_item_name_to_image(self, img, item_name, barcode_text):
        """Add item name above the barcode with appropriate font size for paper type"""
        try:
            # Only add space for item name if it exists
            if not (item_name and item_name.strip()):
                return img
            
            # Different settings for thermal vs standard labels
            if self.page_size == '50x25mm Label':
                # Thermal label settings - more space for text
                extra_height = 35  # More space for thermal labels to show item name clearly
                barcode_y = 30    # Position barcode lower to make room for text above
                font_size = self.item_name_font_size or 14  # Larger font for better visibility on thermal
            else:
                # Standard paper settings - large text
                extra_height = 60  # Increased space for much larger font (24pt)
                barcode_y = 60
                font_size = self.item_name_font_size or 24  # Increased default to 24pt for A4
                
            new_height = img.height + extra_height
            new_img = Image.new('RGB', (img.width, new_height), 'white')
            
            # Position the barcode image (leave space at top for item name)
            new_img.paste(img, (0, barcode_y))
            
            # Add item name text
            draw = ImageDraw.Draw(new_img)
            
            # Try to use appropriate font with configurable size
            try:
                # Try to load TrueType font if available
                try:
                    # Try common system font paths
                    item_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
                except:
                    try:
                        # Linux font path
                        item_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
                    except:
                        try:
                            # Windows font path
                            item_font = ImageFont.truetype("arial.ttf", font_size)
                        except:
                            try:
                                # Alternative Linux fonts
                                item_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", font_size)
                            except:
                                # Fallback to default
                                item_font = ImageFont.load_default()
            except:
                item_font = None
            
            # Add item name at the top
            if item_name and item_name.strip():
                # Truncate long item names to fit width
                max_chars = 25 if self.page_size == '50x25mm Label' else 35
                display_name = item_name[:max_chars] + "..." if len(item_name) > max_chars else item_name
                
                # Calculate text position (centered)
                text_bbox = draw.textbbox((0, 0), display_name, font=item_font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = max(0, (img.width - text_width) // 2)
                
                # Position text differently for thermal vs standard
                if self.page_size == '50x25mm Label':
                    # For thermal labels - text at top with more margin
                    text_y = 5  # Close to top
                else:
                    # For standard labels
                    text_y = 12
                
                # Draw item name with larger font and more top margin
                draw.text((text_x, text_y), display_name, fill='black', font=item_font)
            
            return new_img
        except Exception as e:
            frappe.log_error(f"Error adding text to image: {str(e)}")
            return img

    def add_text_to_image(self, img, text):
        """Add text below barcode image (fallback method)"""
        try:
            # Create new image with extra space for text
            new_height = img.height + 30
            new_img = Image.new('RGB', (img.width, new_height), 'white')
            
            # Paste original image
            new_img.paste(img, (0, 0))
            
            # Add text
            draw = ImageDraw.Draw(new_img)
            
            # Try to use a font, fallback to default
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            # Calculate text position (centered)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (img.width - text_width) // 2
            
            # More spacing for thermal labels to prevent overlap
            if self.page_size == '50x25mm Label':
                text_y = img.height + 8  # More space for thermal labels
            else:
                text_y = img.height + 5  # Standard spacing
            
            draw.text((text_x, text_y), text, fill='black', font=font)
            
            return new_img
        except:
            return img

    def create_error_image(self, code_text, error_msg):
        """Create an error placeholder image"""
        img = Image.new('RGB', (200, 100), 'white')
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 199, 99], outline='red', width=2)
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
            
        draw.text((10, 10), f"Error: {code_text}"[:20], fill='red', font=font)
        draw.text((10, 30), "Invalid code", fill='red', font=font)
        return img

    def create_pdf(self):
        """Generate PDF with all barcodes including item names"""
        try:
            self.generation_status = "In Progress"
            self.save()
            frappe.db.commit()
            
            codes = self.parse_input_data()
            if not codes:
                frappe.throw("No codes to generate")
            
            # Generate all barcode images first
            barcode_images = []
            for i, (item_name, barcode_num) in enumerate(codes):
                img = self.generate_barcode_image(barcode_num, item_name)
                if img:
                    barcode_images.append((item_name, barcode_num, img))
                
                # Update progress for long operations
                if i % 50 == 0:
                    frappe.publish_progress(
                        percent=(i / len(codes)) * 50,  # 50% for image generation
                        title="Generating barcodes...",
                        description=f"Processing {i+1} of {len(codes)} codes"
                    )
            
            # Create PDF
            buffer = io.BytesIO()
            page_size = self.get_page_size()
            c = canvas.Canvas(buffer, pagesize=page_size)
            
            page_width, page_height = page_size
            
            # Handle thermal labels differently
            if self.page_size == '50x25mm Label':
                # For 50x25mm thermal labels - one barcode per label
                margin = 1 * mm  # Minimal margin for thermal labels
                codes_per_row = 1
                codes_per_page = 1
                
                # Use user-specified dimensions for thermal labels
                barcode_width = (self.barcode_width or 40) * mm   # Use form value or default 40mm
                barcode_height = (self.barcode_height or 8) * mm  # Use form value or default 8mm
                
                # Calculate space needed for text based on font size
                font_size = self.item_name_font_size or 12
                text_space = max(6 * mm, font_size * 0.5 * mm)  # Ensure enough space for text
                item_height = barcode_height + text_space + (2 * mm)  # Add padding
                
                x_spacing = page_width
                y_spacing = page_height
                
            else:
                # Standard paper sizes (A4, A5, Letter, Legal) - optimized for maximum density
                margin = 15 * mm  # Reduced margin
                codes_per_row = self.codes_per_row or 3
                
                # Optimized barcode dimensions for standard papers
                standard_barcode_width = 35 * mm   # Slightly smaller width for better fit
                standard_barcode_height = 15 * mm  # Optimized height for density
                
                # Use custom dimensions if specified, otherwise use optimized standards
                barcode_width = (self.barcode_width * mm) if self.barcode_width else standard_barcode_width
                barcode_height = (self.barcode_height * mm) if self.barcode_height else standard_barcode_height
                
                # Minimal padding for maximum density - just enough for text
                font_size = self.item_name_font_size or 24
                text_space = max(8 * mm, font_size * 0.4 * mm)  # Minimal text space
                item_height = barcode_height + text_space + (3 * mm)  # Minimal total height
                
                # Calculate positions with minimal spacing
                available_width = page_width - (2 * margin)
                available_height = page_height - (2 * margin)
                
                # Minimal spacing for maximum density
                x_spacing = available_width / codes_per_row
                y_spacing = item_height + (5 * mm)  # Minimal vertical spacing between rows
                
                codes_per_page = int(available_height / y_spacing) * codes_per_row
            
            for i, (item_name, barcode_num, img) in enumerate(barcode_images):
                # Check if we need a new page
                if self.page_size == '50x25mm Label':
                    # For thermal labels - each label gets its own page
                    if i > 0:  # Start new page for every label after the first
                        c.showPage()
                else:
                    # For standard paper - use grid layout
                    if i > 0 and i % codes_per_page == 0:
                        c.showPage()
                
                if self.page_size == '50x25mm Label':
                    # For thermal labels - position barcode with space for text below
                    x = (page_width - barcode_width) / 2  # Center horizontally
                    
                    # Position barcode in upper portion to leave space for text
                    available_height = page_height - (2 * mm)  # Leave margins
                    barcode_space = barcode_height
                    text_space = max(6 * mm, (self.item_name_font_size or 12) * 0.5 * mm)
                    
                    # Position barcode from top, leaving space for text below
                    y = page_height - margin - barcode_height - (2 * mm)  # From top with margin
                else:
                    # Standard paper positioning
                    # Calculate position in grid with better centering
                    row = (i % codes_per_page) // codes_per_row
                    col = (i % codes_per_page) % codes_per_row
                    
                    # Center barcodes within their allocated space
                    x = margin + (col * x_spacing) + ((x_spacing - barcode_width) / 2)
                    y = page_height - margin - ((row + 1) * y_spacing) + ((y_spacing - item_height) / 2)
                
                # Draw barcode image with item name and barcode number
                try:
                    # Convert to RGB if needed
                    if img.mode == 'RGBA':
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        rgb_img.paste(img, mask=img.split()[-1])
                        img = rgb_img
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Draw image with optimized dimensions
                    c.drawInlineImage(
                        img,  # Pass PIL Image directly
                        x, y, 
                        width=barcode_width, 
                        height=barcode_height,  # Use actual barcode height, not item_height
                        preserveAspectRatio=True
                    )
                except Exception as img_error:
                    # Fallback: draw a rectangle with text
                    c.setStrokeColor('red')
                    c.rect(x, y, barcode_width, item_height)
                    c.drawString(x + 5, y + (item_height/2), f"Error: {barcode_num}")
                    frappe.log_error(f"Image drawing error for {barcode_num}: {str(img_error)}")
                
                # Update progress
                if i % 20 == 0:
                    frappe.publish_progress(
                        percent=50 + ((i / len(barcode_images)) * 50),  # 50-100% for PDF generation
                        title="Creating PDF...",
                        description=f"Adding {i+1} of {len(barcode_images)} barcodes to PDF"
                    )
            
            c.save()
            buffer.seek(0)
            
            # Save as attachment
            file_name = f"barcodes_{self.name}.pdf"
            
            # Create file record
            file_doc = frappe.get_doc({
                "doctype": "File",
                "file_name": file_name,
                "content": buffer.getvalue(),
                "attached_to_doctype": self.doctype,
                "attached_to_name": self.name,
                "is_private": 0
            })
            file_doc.save()
            
            # Update document
            self.generated_pdf = file_doc.file_url
            self.generation_status = "Completed"
            self.generated_on = now_datetime()
            self.save()
            
            frappe.publish_progress(
                percent=100,
                title="Complete!",
                description=f"Successfully generated PDF with {len(barcode_images)} barcodes"
            )
            
            return file_doc.file_url
            
        except Exception as e:
            self.generation_status = "Failed"
            self.save()
            frappe.log_error(f"PDF generation failed: {str(e)}")
            frappe.throw(f"Failed to generate PDF: {str(e)}")

# API Methods remain the same...
@frappe.whitelist()
def generate_pdf(doc_name):
    """API method to generate PDF"""
    try:
        doc = frappe.get_doc("Bulk Barcode Generator", doc_name)
        if not doc.has_permission("write"):
            frappe.throw("Insufficient permissions")
        
        file_url = doc.create_pdf()
        return {
            "success": True,
            "file_url": file_url,
            "message": "PDF generated successfully"
        }
    except Exception as e:
        frappe.log_error(f"API generate_pdf failed: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }

@frappe.whitelist()
def preview_codes(input_data):
    """Preview first few codes from input data with improved parsing"""
    try:
        codes = []
        for line in input_data.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # More flexible parsing to handle different formats
            if ',' in line:
                # CSV format: Item Name,Barcode
                parts = line.split(',', 1)
                if len(parts) == 2:
                    item_name = parts[0].strip()
                    barcode_num = parts[1].strip()
                    if item_name and barcode_num:
                        codes.append(f"{item_name} → {barcode_num}")
                    elif barcode_num:
                        codes.append(f"(No Item Name) → {barcode_num}")
                    else:
                        codes.append(f"(Invalid Entry) → {line}")
                else:
                    # Single value in CSV format line
                    clean_line = line.replace(',', '').strip()
                    if clean_line:
                        codes.append(f"(No Item Name) → {clean_line}")
                        
            elif '\t' in line:
                # Tab-separated: Item Name\tBarcode
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    item_name = parts[0].strip()
                    barcode_num = parts[1].strip()
                    if item_name and barcode_num:
                        codes.append(f"{item_name} → {barcode_num}")
                    elif barcode_num:
                        codes.append(f"(No Item Name) → {barcode_num}")
                    else:
                        codes.append(f"(Invalid Entry) → {line}")
                else:
                    clean_line = line.replace('\t', '').strip()
                    if clean_line:
                        codes.append(f"(No Item Name) → {clean_line}")
                        
            elif '|' in line:
                # Pipe-separated: Item Name | Barcode
                parts = line.split('|', 1)
                if len(parts) == 2:
                    item_name = parts[0].strip()
                    barcode_num = parts[1].strip()
                    if item_name and barcode_num:
                        codes.append(f"{item_name} → {barcode_num}")
                    elif barcode_num:
                        codes.append(f"(No Item Name) → {barcode_num}")
                    else:
                        codes.append(f"(Invalid Entry) → {line}")
                else:
                    clean_line = line.replace('|', '').strip()
                    if clean_line:
                        codes.append(f"(No Item Name) → {clean_line}")
            else:
                # Plain barcode number or unrecognized format
                clean_line = line.strip()
                if clean_line:
                    # Check if it looks like a valid barcode (numbers, letters, some special chars)
                    if re.match(r'^[A-Za-z0-9\-_\.]+$', clean_line):
                        codes.append(f"(No Item Name) → {clean_line}")
                    else:
                        # If it contains spaces, treat first part as item name, rest as barcode
                        parts = clean_line.split(' ', 1)
                        if len(parts) == 2 and re.match(r'^[A-Za-z0-9\-_\.]+$', parts[1].replace(' ', '')):
                            codes.append(f"{parts[0]} → {parts[1]}")
                        else:
                            codes.append(f"(No Item Name) → {clean_line}")
        
        # Return first 10 codes for preview
        return {
            "success": True,
            "codes": codes[:10],
            "total_count": len(codes),
            "has_more": len(codes) > 10,
            "format_info": "Supported formats: 'Item Name,Barcode' or 'Item Name | Barcode' or just 'Barcode'"
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

@frappe.whitelist()
def download_template():
    """Generate and download a sample CSV template"""
    try:
        # Create sample data
        sample_data = [
            ["Item Name", "Barcode Number"],
            ["1/2 PIPE CPVC NIPRO", "01192202500024"],
            ["3/4 ELBOW CPVC", "01192202500025"],
            ["TEE JOINT CPVC", "01192202500026"],
            ["COUPLING CPVC", "01192202500027"],
            ["VALVE BALL 1/2", "01192202500028"]
        ]
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(sample_data)
        
        # Convert to bytes
        csv_content = output.getvalue().encode('utf-8')
        
        # Create file
        frappe.local.response.filename = "barcode_template.csv"
        frappe.local.response.filecontent = csv_content
        frappe.local.response.type = "download"
        
        return {
            "success": True,
            "message": "Template downloaded successfully"
        }
        
    except Exception as e:
        frappe.throw(f"Error generating template: {str(e)}")