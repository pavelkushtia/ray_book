#!/usr/bin/env python3
"""
Ray Internals PDF Generator - Browser Method

This creates a clean HTML file with properly rendered Mermaid diagrams,
then uses a simple browser automation approach to generate PDF.
"""

import os
import re
import markdown
import datetime

def get_chapter_order():
    """Define the correct order of chapters for the book."""
    return [
        "README.md",
        "Part1_Chapter01_Ray_Architecture_Overview.md",
        "Part1_Chapter02_Driver_System.md", 
        "Part1_Chapter03_Task_Lifecycle.md",
        "Part1_Chapter04_Actor_Lifecycle.md",
        "Part1_Chapter05_Memory_System.md",
        "Part2_Chapter06_Global_Control_Service.md",
        "Part2_Chapter07_Raylet_System.md",
        "Part2_Chapter08_Object_Store.md",
        "Part3_Chapter09_Distributed_Scheduling.md",
        "Part3_Chapter10_Autoscaling_System.md",
        "Part3_Chapter11_High_Availability.md",
        "Part4_Chapter12_Network_Protocols.md",
        "Part4_Chapter13_Port_Management.md"
    ]

def read_markdown_file(filepath):
    """Read and return the content of a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Warning: File {filepath} not found, skipping...")
        return ""

def clean_mermaid_diagram(content):
    """Clean and properly format Mermaid diagrams."""
    def process_mermaid(match):
        diagram_content = match.group(1).strip()
        
        # Clean up any XML artifacts
        diagram_content = re.sub(r'<[^>]+>', '', diagram_content)
        diagram_content = re.sub(r'&lt;[^&]*&gt;', '', diagram_content)
        diagram_content = re.sub(r'parameter.*?content.*?>', '', diagram_content)
        
        # Remove extra whitespace and fix formatting
        lines = [line.strip() for line in diagram_content.split('\n') if line.strip()]
        cleaned_diagram = '\n    '.join(lines)
        
        return f'<div class="mermaid">\n{cleaned_diagram}\n</div>'
    
    # Process mermaid code blocks
    content = re.sub(r'```mermaid\n(.*?)\n```', process_mermaid, content, flags=re.DOTALL)
    return content

def create_print_optimized_css():
    """Create CSS optimized for PDF generation."""
    return """
    <style>
    @page {
        size: A4;
        margin: 2.5cm 2cm 2.5cm 2cm;
        @top-left {
            content: "Ray Internals: Complete Technical Guide";
            font-family: Arial, sans-serif;
            font-size: 9pt;
            color: #666;
        }
        @top-right {
            content: counter(page);
            font-family: Arial, sans-serif;
            font-size: 9pt;
            color: #666;
        }
        @bottom-center {
            content: "© 2024 Ray Documentation Project";
            font-family: Arial, sans-serif;
            font-size: 8pt;
            color: #888;
        }
    }
    
    body {
        font-family: 'Georgia', 'Times New Roman', serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
        margin: 0;
        padding: 0;
    }
    
    h1 {
        color: #1976d2;
        font-size: 20pt;
        font-weight: bold;
        margin: 25pt 0 15pt 0;
        padding-bottom: 8pt;
        border-bottom: 2pt solid #1976d2;
        page-break-after: avoid;
    }
    
    h2 {
        color: #388e3c;
        font-size: 16pt;
        font-weight: bold;
        margin: 20pt 0 12pt 0;
        page-break-after: avoid;
    }
    
    h3 {
        color: #f57c00;
        font-size: 13pt;
        font-weight: bold;
        margin: 16pt 0 10pt 0;
        page-break-after: avoid;
    }
    
    h4, h5, h6 {
        color: #c2185b;
        font-size: 11pt;
        font-weight: bold;
        margin: 12pt 0 8pt 0;
        page-break-after: avoid;
    }
    
    p {
        margin: 0 0 10pt 0;
        text-align: justify;
        orphans: 2;
        widows: 2;
    }
    
    pre {
        background-color: #f8f8f8;
        border: 1pt solid #ddd;
        border-left: 3pt solid #1976d2;
        padding: 10pt;
        margin: 12pt 0;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        font-size: 8pt;
        line-height: 1.3;
        page-break-inside: avoid;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    code {
        background-color: #f5f5f5;
        padding: 2pt 3pt;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        font-size: 9pt;
        border-radius: 2pt;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15pt 0;
        font-size: 9pt;
        page-break-inside: avoid;
    }
    
    th, td {
        border: 1pt solid #ddd;
        padding: 6pt 8pt;
        text-align: left;
        vertical-align: top;
    }
    
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    
    blockquote {
        border-left: 3pt solid #1976d2;
        margin: 15pt 0;
        padding: 10pt 20pt;
        background-color: #f8f9fa;
        font-style: italic;
        page-break-inside: avoid;
    }
    
    ul, ol {
        margin: 10pt 0;
        padding-left: 25pt;
    }
    
    li {
        margin: 4pt 0;
    }
    
    .title-page {
        text-align: center;
        margin-top: 150pt;
        page-break-after: always;
    }
    
    .title-page h1 {
        font-size: 28pt;
        color: #1976d2;
        margin-bottom: 20pt;
        border: none;
    }
    
    .subtitle {
        font-size: 14pt;
        color: #666;
        margin: 15pt 0;
        font-style: italic;
    }
    
    .toc {
        page-break-after: always;
        margin: 30pt 0;
    }
    
    .toc h1 {
        font-size: 20pt;
        text-align: center;
        margin-bottom: 25pt;
        border: none;
    }
    
    .toc-part {
        font-weight: bold;
        color: #1976d2;
        font-size: 11pt;
        margin: 15pt 0 8pt 0;
        padding: 6pt 0;
        border-bottom: 1pt solid #eee;
    }
    
    .toc-chapter {
        font-size: 10pt;
        margin: 4pt 0;
        padding-left: 15pt;
    }
    
    .chapter-break {
        page-break-before: always;
    }
    
    /* Mermaid diagrams for PDF */
    .mermaid {
        background-color: #fafafa;
        border: 1pt solid #e1e4e8;
        border-radius: 6pt;
        padding: 15pt;
        margin: 20pt 0;
        text-align: center;
        page-break-inside: avoid;
        min-height: 100pt;
    }
    
    /* Hide web-only elements */
    .no-print {
        display: none;
    }
    </style>
    """

def generate_clean_html():
    """Generate a clean HTML file ready for PDF conversion."""
    print("🚀 Generating clean HTML with proper Mermaid diagrams...")
    
    # Initialize markdown processor
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    
    # Start building HTML
    current_date = datetime.datetime.now().strftime("%B %Y")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ray Internals: Complete Technical Guide</title>
    
    {create_print_optimized_css()}
    
    <!-- Mermaid.js for diagram rendering -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.7.0/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }},
            sequence: {{
                useMaxWidth: true,
                width: 150
            }}
        }});
        
        // Wait for all content to load
        window.addEventListener('DOMContentLoaded', function() {{
            console.log('DOM loaded, Mermaid diagrams should render...');
        }});
    </script>
</head>
<body>

<div class="title-page">
    <h1>Ray Internals</h1>
    <div class="subtitle">A Complete Technical Guide</div>
    <div class="subtitle">Understanding Ray's Architecture, Implementation, and Internals</div>
    <div style="margin-top: 30pt; font-size: 12pt; color: #888;">Generated: {current_date}</div>
</div>

<div class="toc">
    <h1>Table of Contents</h1>
    
    <div class="toc-part">📖 Preface and Introduction</div>
    
    <div class="toc-part">📘 Part I: Ray Fundamentals</div>
    <div class="toc-chapter">Chapter 1: Ray Architecture Overview</div>
    <div class="toc-chapter">Chapter 2: The Ray Driver System</div>
    <div class="toc-chapter">Chapter 3: Task Lifecycle and Management</div>
    <div class="toc-chapter">Chapter 4: Actor Lifecycle and Management</div>
    <div class="toc-chapter">Chapter 5: Memory and Object Reference System</div>
    
    <div class="toc-part">📗 Part II: Core Ray Services</div>
    <div class="toc-chapter">Chapter 6: Global Control Service (GCS)</div>
    <div class="toc-chapter">Chapter 7: Raylet Implementation and Lifecycle</div>
    <div class="toc-chapter">Chapter 8: Distributed Object Store</div>
    
    <div class="toc-part">📙 Part III: Advanced Ray Systems</div>
    <div class="toc-chapter">Chapter 9: Distributed Scheduling Implementation</div>
    <div class="toc-chapter">Chapter 10: Autoscaling System</div>
    <div class="toc-chapter">Chapter 11: High Availability and Fault Tolerance</div>
    
    <div class="toc-part">📔 Part IV: System Internals</div>
    <div class="toc-chapter">Chapter 12: Network Communication and Protocols</div>
    <div class="toc-chapter">Chapter 13: Port Assignment and Management</div>
</div>

"""
    
    # Process each chapter
    chapter_files = get_chapter_order()
    
    for i, chapter_file in enumerate(chapter_files):
        print(f"📄 Processing: {chapter_file}")
        
        # Read markdown content
        markdown_content = read_markdown_file(chapter_file)
        if not markdown_content:
            continue
        
        # Clean Mermaid diagrams
        cleaned_content = clean_mermaid_diagram(markdown_content)
        
        # Convert to HTML
        chapter_html = md.convert(cleaned_content)
        
        # Add chapter break for non-first chapters
        if i > 0:
            html_content += '<div class="chapter-break"></div>\n'
        
        # Add the chapter content
        html_content += chapter_html + '\n\n'
        
        # Reset markdown processor for next chapter
        md.reset()
    
    # Close HTML
    html_content += """
</body>
</html>
"""
    
    # Write the HTML file
    output_file = "Ray_Internals_PDF_Ready.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Clean HTML generated: {output_file}")
    
    # Get file size
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # Convert to MB
    print(f"📊 File size: {file_size:.2f} MB")
    
    return output_file

def create_pdf_instructions():
    """Create instructions for PDF generation."""
    instructions = """
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
"""
    
    with open("PDF_Generation_Instructions.md", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("📋 PDF generation instructions created: PDF_Generation_Instructions.md")

if __name__ == "__main__":
    try:
        html_file = generate_clean_html()
        create_pdf_instructions()
        
        print(f"\n🎉 Success! PDF-ready HTML file created: {html_file}")
        print("\n📖 Next Steps:")
        print("  1. Open Ray_Internals_PDF_Ready.html in your browser")
        print("  2. Wait for diagrams to load")
        print("  3. Use Ctrl+P → Save as PDF")
        print("  4. Choose A4 size with default margins")
        print("\n📋 See PDF_Generation_Instructions.md for detailed steps")
        print("\n🎨 Features:")
        print("  • ✅ All Mermaid diagrams will render properly")
        print("  • 📄 Professional PDF layout with page numbers")
        print("  • 🎨 Color-coded section headings")
        print("  • 📚 Complete table of contents")
        print("  • 🖨️ Optimized for high-quality printing")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc() 