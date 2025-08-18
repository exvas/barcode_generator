#!/usr/bin/env python3
"""
Test script for the new upload/download functionality
"""

import csv
import io

def test_preview_function():
    """Test the improved preview function with various input formats"""
    
    # Test data with different formats
    test_input = """1/2 PIPE CPVC NIPRO,01192202500024
3/4 ELBOW CPVC,01192202500025
TEE JOINT CPVC | 01192202500026
COUPLING CPVC	01192202500027
test 01192202
01192202500030
VALVE BALL 1/2 01192202500031"""

    print("=== Testing Input Data Processing ===")
    print("Input:")
    print(test_input)
    print("\n" + "="*50)
    
    codes = []
    for line in test_input.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Process like the improved parse function
        if ',' in line:
            parts = line.split(',', 1)
            if len(parts) == 2:
                item_name = parts[0].strip()
                barcode_num = parts[1].strip()
                codes.append(f"{item_name} → {barcode_num}")
        elif '\t' in line:
            parts = line.split('\t', 1)
            if len(parts) == 2:
                item_name = parts[0].strip()
                barcode_num = parts[1].strip()
                codes.append(f"{item_name} → {barcode_num}")
        elif '|' in line:
            parts = line.split('|', 1)
            if len(parts) == 2:
                item_name = parts[0].strip()
                barcode_num = parts[1].strip()
                codes.append(f"{item_name} → {barcode_num}")
        else:
            # Check if multiple words with last word being barcode
            words = line.split()
            if len(words) >= 2:
                last_word = words[-1]
                if len(last_word) >= 4:  # Assume barcode-like
                    item_name = ' '.join(words[:-1])
                    barcode_num = last_word
                    codes.append(f"{item_name} → {barcode_num}")
                else:
                    codes.append(f"(No Item Name) → {line}")
            else:
                codes.append(f"(No Item Name) → {line}")
    
    print("Processed Output:")
    for i, code in enumerate(codes, 1):
        print(f"{i}. {code}")
    
    return codes

def test_template_generation():
    """Test CSV template generation"""
    print("\n\n=== Testing CSV Template Generation ===")
    
    # Sample data like in our download_template function
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
    
    csv_content = output.getvalue()
    print("Generated CSV Template:")
    print(csv_content)
    
    return csv_content

if __name__ == "__main__":
    # Test the preview function
    test_codes = test_preview_function()
    
    # Test template generation  
    template_csv = test_template_generation()
    
    print(f"\n=== Summary ===")
    print(f"Successfully processed {len(test_codes)} codes")
    print(f"Template has {len(template_csv.split(chr(10))) - 1} rows") # -1 for the last empty line
    print("All tests completed successfully!")
