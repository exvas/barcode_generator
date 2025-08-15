# Debug Thermal Label Issue

## 🔍 **Debugging Thermal Label Skipping**

The issue appears to be that while the PDF logic is correct (each barcode gets its own page), the thermal labels are still showing gaps when printed.

## 🧪 **Possible Causes:**

1. **PDF Page Size Issue**: The 50x25mm page size might not match the actual thermal label size
2. **Printer Driver Issue**: TA-P05 printer might be interpreting the PDF differently
3. **Margin/Positioning Issue**: Content might not be positioned correctly on the thermal label

## 🔧 **Debug Steps:**

### Step 1: Verify PDF Structure
1. Generate a few test barcodes
2. Open the PDF and check:
   - Number of pages matches number of barcodes
   - Each page has exactly one barcode
   - Page size is correct (50x25mm)

### Step 2: Check Printer Settings
1. TA-P05 printer settings:
   - Paper size: 50mm x 25mm
   - Print quality: High
   - Scaling: 100% (no fit-to-page)

### Step 3: Test Different Dimensions
Try these alternative settings:

| Setting | Option A | Option B | Option C |
|---------|----------|----------|----------|
| Page Size | 50x25mm Label | 50x25mm Label | 50x25mm Label |
| Barcode Width | 38mm | 35mm | 40mm |
| Barcode Height | 8mm | 6mm | 10mm |
| Font Size | 12pt | 10pt | 14pt |

### Step 4: Printer Test
1. Print a single barcode first
2. Check if it prints in the correct position
3. Then test multiple barcodes

## 🎯 **Expected vs Actual:**

**Expected:** Each thermal label prints consecutively
**Actual:** Gaps appear between labels

**Next Actions:**
1. Test PDF structure
2. Check printer driver settings
3. Verify label positioning
4. Test with different dimensions
