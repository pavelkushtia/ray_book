#!/usr/bin/env python3
"""
Ray Internals HTML E-book Generator

This script converts all the markdown chapters into a single, nicely formatted HTML e-book
that can be printed to PDF or read in any web browser.
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

def preprocess_markdown(content, chapter_title=""):
    """Preprocess markdown content for better HTML formatting."""
    # Add page break before each new chapter (except the first one)
    if chapter_title and not chapter_title.startswith("README"):
        content = '<div class="page-break"></div>\n\n' + content
    
    # Convert mermaid diagrams to text placeholders (since they won't render in print)
    content = re.sub(r'```mermaid\n(.*?)\n```', 
                    lambda m: f'<div class="diagram-placeholder">📊 Diagram: {m.group(1)[:100]}{"..." if len(m.group(1)) > 100 else ""}</div>', 
                    content, flags=re.DOTALL)
    
    return content

def generate_html_ebook():
    """Generate the complete HTML e-book."""
    print("🚀 Starting Ray Internals HTML E-book generation...")
    
    # Initialize markdown processor
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    
    # CSS styles
    css_styles = """
    <style>
    body {
        font-family: 'Georgia', 'Times New Roman', serif;
        line-height: 1.6;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    @media print {
        body { font-size: 12pt; margin: 0; padding: 0.5in; }
        .page-break { page-break-before: always; }
        .no-print { display: none; }
        h1, h2, h3 { page-break-after: avoid; }
    }
    
    h1 { color: #1976d2; font-size: 2.5em; margin: 40px 0 30px 0; border-bottom: 3px solid #1976d2; padding-bottom: 15px; }
    h2 { color: #388e3c; font-size: 2em; margin: 35px 0 25px 0; }
    h3 { color: #f57c00; font-size: 1.5em; margin: 30px 0 20px 0; }
    h4, h5, h6 { color: #c2185b; font-size: 1.2em; margin: 25px 0 15px 0; }
    
    code {
        background-color: #f5f5f5;
        padding: 3px 6px;
        border-radius: 4px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        font-size: 0.9em;
        color: #d73a49;
    }
    
    pre {
        background-color: #f8f8f8;
        border: 1px solid #e1e4e8;
        border-left: 4px solid #1976d2;
        border-radius: 6px;
        padding: 20px;
        margin: 20px 0;
        overflow-x: auto;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        font-size: 0.85em;
        line-height: 1.45;
    }
    
    pre code { background: none; padding: 0; border-radius: 0; color: #333; }
    
    table { width: 100%; border-collapse: collapse; margin: 25px 0; }
    th, td { border: 1px solid #ddd; padding: 12px 15px; text-align: left; }
    th { background-color: #f2f2f2; font-weight: bold; }
    
    blockquote {
        border-left: 4px solid #1976d2;
        margin: 25px 0;
        padding: 15px 25px;
        background-color: #f8f9fa;
        font-style: italic;
        color: #555;
    }
    
    .title-page {
        text-align: center;
        padding: 100px 0;
        page-break-after: always;
    }
    
    .title-page h1 {
        font-size: 3.5em;
        color: #1976d2;
        margin-bottom: 30px;
        border: none;
    }
    
    .title-page .subtitle {
        font-size: 1.3em;
        color: #666;
        margin-bottom: 20px;
        font-style: italic;
    }
    
    .toc {
        page-break-after: always;
        padding: 40px 0;
    }
    
    .toc ul { list-style: none; padding-left: 0; }
    .toc .part {
        font-weight: bold;
        color: #1976d2;
        font-size: 1.1em;
        margin: 25px 0 10px 0;
        padding: 10px 0;
        border-bottom: 1px solid #eee;
    }
    .toc .chapter {
        color: #333;
        margin: 8px 0;
        padding-left: 25px;
    }
    
    .diagram-placeholder {
        background-color: #e3f2fd;
        border: 2px dashed #1976d2;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
        color: #1976d2;
        font-weight: bold;
    }
    
    .chapter-separator {
        height: 2px;
        background: linear-gradient(to right, #1976d2, transparent);
        margin: 50px 0;
        page-break-after: always;
    }
    </style>
    """
    
    # Start building HTML
    current_date = datetime.datetime.now().strftime("%B %Y")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ray Internals: A Comprehensive Technical Guide</title>
    {css_styles}
</head>
<body>

<div class="title-page">
    <h1>Ray Internals</h1>
    <div class="subtitle">A Comprehensive Technical Guide</div>
    <div class="subtitle">The Complete Guide to Understanding Ray's Architecture, Implementation, and Internals</div>
    <div style="margin-top: 40px; color: #888;">Generated: {current_date}</div>
</div>

<div class="no-print" style="background: #e8f5e8; padding: 15px; margin: 20px 0; border-radius: 8px;">
    <h3 style="color: #2e7d32; margin-top: 0;">📱 How to Use This E-book</h3>
    <ul style="margin: 10px 0; color: #2e7d32;">
        <li><strong>Print to PDF:</strong> Use Ctrl+P → Save as PDF for offline reading</li>
        <li><strong>Search:</strong> Use Ctrl+F to find specific topics</li>
        <li><strong>Navigate:</strong> Use the table of contents below</li>
    </ul>
</div>

<div class="toc">
    <h1>Table of Contents</h1>
    <ul>
        <li class="part">📖 Preface and Introduction</li>
        
        <li class="part">📘 Part I: Ray Fundamentals</li>
        <li class="chapter">Chapter 1: Ray Architecture Overview</li>
        <li class="chapter">Chapter 2: The Ray Driver System</li>
        <li class="chapter">Chapter 3: Task Lifecycle and Management</li>
        <li class="chapter">Chapter 4: Actor Lifecycle and Management</li>
        <li class="chapter">Chapter 5: Memory and Object Reference System</li>
        
        <li class="part">📗 Part II: Core Ray Services</li>
        <li class="chapter">Chapter 6: Global Control Service (GCS)</li>
        <li class="chapter">Chapter 7: Raylet Implementation and Lifecycle</li>
        <li class="chapter">Chapter 8: Distributed Object Store</li>
        
        <li class="part">📙 Part III: Advanced Ray Systems</li>
        <li class="chapter">Chapter 9: Distributed Scheduling Implementation</li>
        <li class="chapter">Chapter 10: Autoscaling System</li>
        <li class="chapter">Chapter 11: High Availability and Fault Tolerance</li>
        
        <li class="part">📔 Part IV: System Internals</li>
        <li class="chapter">Chapter 12: Network Communication and Protocols</li>
        <li class="chapter">Chapter 13: Port Assignment and Management</li>
    </ul>
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
            
        # Preprocess the content
        processed_content = preprocess_markdown(markdown_content, chapter_file)
        
        # Convert to HTML
        chapter_html = md.convert(processed_content)
        
        # Add chapter separator (except for first chapter)
        if i > 0:
            html_content += '<div class="chapter-separator"></div>\n'
        
        # Add the chapter content
        html_content += chapter_html + '\n\n'
        
        # Reset markdown processor for next chapter
        md.reset()
    
    # Close HTML
    html_content += """
</body>
</html>
"""
    
    # Write to file
    output_file = "Ray_Internals_Complete_Guide.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML e-book generated successfully: {output_file}")
    
    # Get file size
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # Convert to MB
    print(f"📊 File size: {file_size:.2f} MB")
    
    return output_file

if __name__ == "__main__":
    try:
        html_file = generate_html_ebook()
        print(f"\n🎉 Success! Your Ray Internals e-book is ready: {html_file}")
        print("\n📖 How to use your e-book:")
        print("  • Open in web browser for digital reading")
        print("  • Print to PDF using browser's print function")
        print("  • Use Ctrl+F to search for specific content")
        print("  • Professional formatting with table of contents")
        print("\n💡 To convert to PDF:")
        print("  1. Open the HTML file in Chrome/Firefox")
        print("  2. Press Ctrl+P (Cmd+P on Mac)")
        print("  3. Select 'Save as PDF' as destination")
        print("  4. Choose appropriate print settings and save")
    except Exception as e:
        print(f"❌ Error generating HTML e-book: {str(e)}")
        import traceback
        traceback.print_exc() 