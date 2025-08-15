# Quick Test for Thermal Label Issue

## 🧪 **Simple Test to Isolate the Problem**

Let's test with just 2 barcodes to see exactly what happens:

### Test Input:
```
Test1,0010251279
Test2,0010251280
```

### Expected PDF Structure:
- Page 1: "Test1" + barcode "0010251279"
- Page 2: "Test2" + barcode "0010251280"
- Total: 2 pages

### Expected Print Result:
- Label 1: Test1 barcode
- Label 2: Test2 barcode
- No gaps between labels

### If Still Skipping:
The issue might be:
1. **Printer Driver**: TA-P05 driver interpreting PDF incorrectly
2. **PDF Format**: Page format not matching thermal printer expectations
3. **Print Settings**: Scaling or fit-to-page causing issues

### Alternative Solutions:

#### Option 1: Different Page Size
Try using a custom page size that matches your thermal printer exactly:
- Width: 50mm = 141.732 points
- Height: 25mm = 70.866 points

#### Option 2: Print Settings
In your printer settings, try:
- Scale: 100% (no scaling)
- Page handling: Actual size
- Paper source: Manual feed
- Quality: High

#### Option 3: Test with Single Page
Generate just ONE barcode and see if it prints correctly positioned.

### Printer-Specific Troubleshooting:
For TA-P05 thermal printers:
1. Check if "continuous paper" mode is enabled
2. Verify label sensor is working
3. Test with different print speeds
4. Check if printer is detecting label gaps correctly
