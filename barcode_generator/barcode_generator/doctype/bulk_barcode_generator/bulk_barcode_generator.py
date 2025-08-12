# Enhanced version of bulk_barcode_generator.py to support item names

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_site_path
import os
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter, A3, A5, legal
from reportlab.lib.units import mm
import qrcode
import re

class BulkBarcodeGenerator(Document):
    def validate(self):
        """Validate input data before saving"""
        if not self.input_data:
            frappe.throw("Input data is required")
        
        # Count total codes
        codes = self.parse_input_data()
        self.total_codes = len(codes)
        
        if self.total_codes == 0:
            frappe.throw("No valid codes found in input data")
        
        if self.total_codes > 1000:
            frappe.throw("Maximum 1000 codes allowed per batch")

    def parse_input_data(self):
        """Parse input data and return list of (item_name, barcode) tuples"""
        if not self.input_data:
            return []
        
        codes = []
        for line in self.input_data.split('\n'):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
                
            # Try to parse different formats:
            # Format 1: "Item Name,Barcode" or "Item Name\tBarcode"
            # Format 2: "Item Name | Barcode"  
            # Format 3: Just "Barcode" (no item name)
            
            if ',' in line:
                # CSV format: Item Name,Barcode
                parts = line.split(',', 1)
                if len(parts) == 2:
                    item_name = parts[0].strip()
                    barcode_num = parts[1].strip()
                    codes.append((item_name, barcode_num))
                else:
                    # Just barcode
                    codes.append(("", line.strip()))
                    
            elif '\t' in line:
                # Tab-separated: Item Name\tBarcode
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    item_name = parts[0].strip()
                    barcode_num = parts[1].strip()
                    codes.append((item_name, barcode_num))
                else:
                    codes.append(("", line.strip()))
                    
            elif '|' in line:
                # Pipe-separated: Item Name | Barcode
                parts = line.split('|', 1)
                if len(parts) == 2:
                    item_name = parts[0].strip()
                    barcode_num = parts[1].strip()
                    codes.append((item_name, barcode_num))
                else:
                    codes.append(("", line.strip()))
            else:
                # Just barcode number
                codes.append(("", line.strip()))
        
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
            'Legal': legal
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
                
                # Create barcode with standard optimized options
                options = {
                    'module_width': 0.33,  # Standard module width in mm (0.33mm is common)
                    'module_height': 10.0,  # Reduced height for bars only
                    'quiet_zone': 3.0,      # Reduced quiet zone for compact layout
                    'font_size': 8,         # Standard font size for readability
                    'text_distance': 3.0,   # More space between bars and text
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
        """Add item name above the barcode with 12pt font size"""
        try:
            # Only add space for item name if it exists
            if not (item_name and item_name.strip()):
                return img
                
            extra_height = 35  # More space for larger font
            new_height = img.height + extra_height
            new_img = Image.new('RGB', (img.width, new_height), 'white')
            
            # Position the barcode image (leave more space at top for larger item name)
            barcode_y = 35
            new_img.paste(img, (0, barcode_y))
            
            # Add item name text
            draw = ImageDraw.Draw(new_img)
            
            # Try to use larger font with configurable size
            try:
                font_size = self.item_name_font_size or 16  # Default to 12pt
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
                display_name = item_name[:35] + "..." if len(item_name) > 35 else item_name
                
                # Calculate text position (centered)
                text_bbox = draw.textbbox((0, 0), display_name, font=item_font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = max(0, (img.width - text_width) // 2)
                
                # Draw item name with larger font
                draw.text((text_x, 8), display_name, fill='black', font=item_font)
            
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
            text_y = img.height + 5
            
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
            margin = 20 * mm
            
            # Calculate layout with standard barcode dimensions
            codes_per_row = self.codes_per_row or 3
            
            # Standard barcode dimensions (optimized to prevent overlap)
            standard_barcode_width = 37 * mm   # Standard width for Code128
            standard_barcode_height = 18 * mm  # Increased height to accommodate text properly
            
            # Use custom dimensions if specified, otherwise use standards
            barcode_width = (self.barcode_width * mm) if self.barcode_width else standard_barcode_width
            barcode_height = (self.barcode_height * mm) if self.barcode_height else standard_barcode_height
            
            # Add padding for larger item name (12pt font)
            item_height = barcode_height + (25 * mm)  # More space for larger font
            
            # Calculate positions with optimized spacing
            available_width = page_width - (2 * margin)
            available_height = page_height - (2 * margin)
            
            # Optimized spacing for standard layout
            x_spacing = available_width / codes_per_row
            y_spacing = item_height + (8 * mm)  # Reduced vertical spacing
            
            codes_per_page = int(available_height / y_spacing) * codes_per_row
            
            for i, (item_name, barcode_num, img) in enumerate(barcode_images):
                # Check if we need a new page
                if i > 0 and i % codes_per_page == 0:
                    c.showPage()
                
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
    """Preview first few codes from input data"""
    try:
        codes = []
        for line in input_data.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if ',' in line:
                parts = line.split(',', 1)
                if len(parts) == 2:
                    codes.append(f"{parts[0].strip()} → {parts[1].strip()}")
                else:
                    codes.append(line)
            elif '\t' in line:
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    codes.append(f"{parts[0].strip()} → {parts[1].strip()}")
                else:
                    codes.append(line)
            elif '|' in line:
                parts = line.split('|', 1)
                if len(parts) == 2:
                    codes.append(f"{parts[0].strip()} → {parts[1].strip()}")
                else:
                    codes.append(line)
            else:
                codes.append(f"(No Item Name) → {line}")
        
        # Return first 10 codes for preview
        return {
            "success": True,
            "codes": codes[:10],
            "total_count": len(codes),
            "has_more": len(codes) > 10
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }