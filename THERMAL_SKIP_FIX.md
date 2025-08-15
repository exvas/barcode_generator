# Fix for Thermal Label Skipping Issue

## 🐛 **Issue Fixed:**
Thermal labels were skipping 2 labels and only printing every 3rd label.

## ✅ **Solution Applied:**
Modified the page logic so that:
- **Thermal Labels (50x25mm)**: Each barcode gets its own page/label
- **Standard Paper (A4, etc.)**: Uses grid layout with multiple barcodes per page

## 🔧 **Code Changes:**
```python
# OLD (causing skipping):
if i > 0 and i % codes_per_page == 0:
    c.showPage()

# NEW (fixed):
if self.page_size == '50x25mm Label':
    # For thermal labels - each label gets its own page
    if i > 0:  # Start new page for every label after the first
        c.showPage()
else:
    # For standard paper - use grid layout
    if i > 0 and i % codes_per_page == 0:
        c.showPage()
```

## 🧪 **Test Your Fix:**

### Test Input:
```
Product A,0010251279
Product B,0010251280  
Product C,0010251281
Product D,0010251282
Product E,0010251283
```

### Expected Result:
- ✅ **5 separate thermal labels** (no skipping)
- ✅ **Each label prints consecutively**
- ✅ **No blank labels between prints**

### Settings to Use:
- Page Size: `50x25mm Label`
- Barcode Width: `38 mm`
- Barcode Height: `8 mm`
- Font Size: `12 pt`

## 🎯 **Verification:**
After generating the PDF:
1. Check PDF has 5 pages (one per barcode)
2. Each page should have one barcode with item name
3. No empty/skipped pages in between

The thermal label skipping issue should now be completely resolved! 🎉
