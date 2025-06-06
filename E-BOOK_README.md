# Ray Internals E-Books

This directory contains professionally formatted e-book versions of the complete Ray Internals documentation.

## 📚 Available Formats

### 1. HTML E-Book (`Ray_Internals_Complete_Guide.html`)
- **Size:** 629 KB
- **Best for:** Web browsers, printing to PDF, digital reading on computers
- **Features:**
  - Professional typography and styling
  - Print-optimized CSS for PDF conversion
  - Table of contents with navigation
  - Syntax-highlighted code blocks
  - Responsive design for different screen sizes

**How to use:**
1. **Digital Reading:** Open the HTML file in any web browser
2. **PDF Conversion:** 
   - Open in Chrome or Firefox
   - Press `Ctrl+P` (or `Cmd+P` on Mac)
   - Select "Save as PDF" as destination
   - Choose "More settings" → enable "Background graphics"
   - Click "Save" to create a PDF version
3. **Search:** Use `Ctrl+F` to search for specific content
4. **Offline Reading:** Save the HTML file locally for offline access

### 2. EPUB E-Book (`Ray_Internals_Complete_Guide.epub`)
- **Size:** 102 KB
- **Best for:** E-readers (Kindle, Nook, Kobo), mobile apps, tablets
- **Features:**
  - Standard EPUB 2.0 format
  - Adjustable font sizes and reading modes
  - Chapter-based navigation
  - Optimized for e-reader devices
  - Compatible with most reading applications

**How to use:**
1. **E-Readers:** Transfer the EPUB file to your e-reader device
2. **Mobile Apps:** Open with apps like Apple Books, Google Play Books, Adobe Digital Editions
3. **Desktop:** Use applications like Calibre, Adobe Digital Editions, or browser extensions
4. **Kindle:** Convert using Calibre or Amazon's email service

## 📖 Book Content

The e-books include all 13 chapters organized in 4 parts:

### 📘 Part I: Ray Fundamentals
- Chapter 1: Ray Architecture Overview
- Chapter 2: The Ray Driver System  
- Chapter 3: Task Lifecycle and Management
- Chapter 4: Actor Lifecycle and Management
- Chapter 5: Memory and Object Reference System

### 📗 Part II: Core Ray Services
- Chapter 6: Global Control Service (GCS)
- Chapter 7: Raylet Implementation and Lifecycle
- Chapter 8: Distributed Object Store

### 📙 Part III: Advanced Ray Systems
- Chapter 9: Distributed Scheduling Implementation
- Chapter 10: Autoscaling System
- Chapter 11: High Availability and Fault Tolerance

### 📔 Part IV: System Internals
- Chapter 12: Network Communication and Protocols
- Chapter 13: Port Assignment and Management

## 🎨 Features

Both e-book formats include:
- ✅ Professional typography and layout
- ✅ Syntax-highlighted code blocks
- ✅ Properly formatted tables and lists
- ✅ Color-coded headings by section type
- ✅ Table of contents for easy navigation
- ✅ Clean, readable formatting optimized for each format

## 🔄 Regenerating E-Books

To regenerate the e-books (if content is updated):

1. **HTML Version:**
   ```bash
   python3 generate_html_ebook.py
   ```

2. **EPUB Version:**
   ```bash
   python3 generate_epub.py
   ```

## 📋 Notes

- Mermaid diagrams from the original markdown are converted to text placeholders in both formats
- All chapters are combined into single files for convenient reading
- The e-books are generated from the latest version of all markdown chapters
- Both formats maintain the professional styling and structure of the original documentation

## 🎯 Recommended Usage

- **For printing or PDF archival:** Use the HTML version
- **For mobile/tablet reading:** Use the EPUB version
- **For sharing digitally:** HTML version works in any browser
- **For e-reader devices:** EPUB version provides the best experience

Both formats provide a complete, professional reading experience of the comprehensive Ray Internals documentation. 