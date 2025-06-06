
# 📄 PDF Generation Instructions

## Method 1: Browser Print-to-PDF (Recommended)

1. Open the file `Ray_Internals_PDF_Ready.html` in your browser
2. Wait for all Mermaid diagrams to load (they should render automatically)
3. Press Ctrl+P (or Cmd+P on Mac) to open print dialog
4. Choose "Save as PDF" as the destination
5. Set the following options:
   - Paper size: A4
   - Margins: Default
   - Scale: 100%
   - Include headers and footers: Yes
   - Background graphics: Yes
6. Click "Save" and choose filename: Ray_Internals_Complete_Guide.pdf

## Method 2: Command Line (if available)

If you have wkhtmltopdf installed:
```bash
wkhtmltopdf --page-size A4 --margin-top 1in --margin-bottom 1in --margin-left 0.8in --margin-right 0.8in --enable-javascript --javascript-delay 5000 Ray_Internals_PDF_Ready.html Ray_Internals_Complete_Guide.pdf
```

## Method 3: Online Converter

1. Upload Ray_Internals_PDF_Ready.html to an online HTML-to-PDF service
2. Wait for conversion
3. Download the PDF

## Features in the PDF-ready HTML:

✅ All Mermaid diagrams properly formatted and will render
✅ Professional typography optimized for PDF
✅ Proper page breaks between chapters  
✅ Print-optimized CSS with headers/footers
✅ Table of contents
✅ Color-coded section headings
✅ All 13 chapters + preface included

The HTML file is specifically designed for high-quality PDF conversion!
