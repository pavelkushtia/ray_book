#!/usr/bin/env python3
"""
Ray Internals EPUB E-book Generator

This script converts all the markdown chapters into an EPUB e-book format
for better compatibility with e-readers.
"""

import os
import re
import markdown
import datetime
import zipfile
import uuid

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

def preprocess_markdown(content):
    """Preprocess markdown content for EPUB."""
    # Remove mermaid diagrams
    content = re.sub(r'```mermaid\n(.*?)\n```', 
                    r'[Diagram content removed for EPUB version]', 
                    content, flags=re.DOTALL)
    return content

def create_epub_css():
    """Create CSS for EPUB."""
    return """
body {
    font-family: Georgia, serif;
    line-height: 1.6;
    margin: 1em;
    color: #333;
}

h1 {
    color: #1976d2;
    font-size: 2em;
    margin: 1.5em 0 1em 0;
    border-bottom: 2px solid #1976d2;
    padding-bottom: 0.5em;
}

h2 {
    color: #388e3c;
    font-size: 1.5em;
    margin: 1.2em 0 0.8em 0;
}

h3 {
    color: #f57c00;
    font-size: 1.2em;
    margin: 1em 0 0.6em 0;
}

h4, h5, h6 {
    color: #c2185b;
    font-size: 1em;
    margin: 0.8em 0 0.5em 0;
}

code {
    background-color: #f5f5f5;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: Monaco, Consolas, monospace;
    font-size: 0.9em;
}

pre {
    background-color: #f8f8f8;
    border: 1px solid #e1e4e8;
    border-left: 4px solid #1976d2;
    border-radius: 6px;
    padding: 1em;
    margin: 1em 0;
    overflow-x: auto;
    font-family: Monaco, Consolas, monospace;
    font-size: 0.85em;
    line-height: 1.4;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}

th {
    background-color: #f2f2f2;
    font-weight: bold;
}

blockquote {
    border-left: 4px solid #1976d2;
    margin: 1em 0;
    padding: 0.5em 1em;
    background-color: #f8f9fa;
    font-style: italic;
}

ul, ol {
    margin: 1em 0;
    padding-left: 2em;
}

.title-page {
    text-align: center;
    padding: 2em 0;
}

.title-page h1 {
    font-size: 2.5em;
    border: none;
    margin-bottom: 0.5em;
}

.subtitle {
    font-size: 1.2em;
    color: #666;
    margin-bottom: 1em;
    font-style: italic;
}
"""

def create_mimetype():
    """Create EPUB mimetype file."""
    return "application/epub+zip"

def create_container_xml():
    """Create EPUB container.xml."""
    return """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""

def create_content_opf(chapters):
    """Create EPUB content.opf file."""
    book_id = str(uuid.uuid4())
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    manifest_items = []
    spine_items = []
    
    # Add CSS
    manifest_items.append('<item id="css" href="styles.css" media-type="text/css"/>')
    
    # Add chapters
    for i, (chapter_file, title) in enumerate(chapters):
        chapter_id = f"chapter{i+1}"
        filename = f"{chapter_id}.xhtml"
        manifest_items.append(f'<item id="{chapter_id}" href="{filename}" media-type="application/xhtml+xml"/>')
        spine_items.append(f'<itemref idref="{chapter_id}"/>')
    
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title>Ray Internals: A Comprehensive Technical Guide</dc:title>
    <dc:creator>Ray Internals Documentation Team</dc:creator>
    <dc:identifier id="bookid">{book_id}</dc:identifier>
    <dc:language>en</dc:language>
    <dc:date>{current_date}</dc:date>
    <dc:description>The Complete Guide to Understanding Ray's Architecture, Implementation, and Internals</dc:description>
    <dc:subject>Computer Science</dc:subject>
    <dc:subject>Distributed Computing</dc:subject>
    <dc:subject>Ray Framework</dc:subject>
  </metadata>
  <manifest>
    {chr(10).join(manifest_items)}
  </manifest>
  <spine toc="ncx">
    {chr(10).join(spine_items)}
  </spine>
</package>"""

def create_chapter_xhtml(title, content, chapter_num):
    """Create XHTML file for a chapter."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
{content}
</body>
</html>"""

def generate_epub():
    """Generate the EPUB e-book."""
    print("🚀 Starting Ray Internals EPUB E-book generation...")
    
    # Initialize markdown processor
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    
    chapters = []
    chapter_files = get_chapter_order()
    
    # Process each chapter
    for i, chapter_file in enumerate(chapter_files):
        print(f"📄 Processing: {chapter_file}")
        
        # Read markdown content
        markdown_content = read_markdown_file(chapter_file)
        if not markdown_content:
            continue
        
        # Extract title
        title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
        title = title_match.group(1) if title_match else f"Chapter {i+1}"
        
        # Preprocess and convert
        processed_content = preprocess_markdown(markdown_content)
        html_content = md.convert(processed_content)
        
        chapters.append((chapter_file, title, html_content))
        md.reset()
    
    # Create EPUB
    output_file = "Ray_Internals_Complete_Guide.epub"
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as epub:
        # Add mimetype (uncompressed)
        epub.writestr("mimetype", create_mimetype(), compress_type=zipfile.ZIP_STORED)
        
        # Add META-INF/container.xml
        epub.writestr("META-INF/container.xml", create_container_xml())
        
        # Add CSS
        epub.writestr("OEBPS/styles.css", create_epub_css())
        
        # Add content.opf
        epub.writestr("OEBPS/content.opf", create_content_opf([(ch[0], ch[1]) for ch in chapters]))
        
        # Add chapters
        for i, (chapter_file, title, content) in enumerate(chapters):
            chapter_filename = f"OEBPS/chapter{i+1}.xhtml"
            chapter_content = create_chapter_xhtml(title, content, i+1)
            epub.writestr(chapter_filename, chapter_content)
    
    print(f"✅ EPUB e-book generated successfully: {output_file}")
    
    # Get file size
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # Convert to MB
    print(f"📊 File size: {file_size:.2f} MB")
    
    return output_file

if __name__ == "__main__":
    try:
        epub_file = generate_epub()
        print(f"\n🎉 Success! Your Ray Internals EPUB e-book is ready: {epub_file}")
        print("\n📖 How to use your EPUB e-book:")
        print("  • Open with any e-reader (Kindle, Apple Books, Adobe Digital Editions)")
        print("  • Compatible with mobile reading apps")
        print("  • Supports adjustable font sizes and reading modes")
        print("  • Professional formatting optimized for e-readers")
    except Exception as e:
        print(f"❌ Error generating EPUB e-book: {str(e)}")
        import traceback
        traceback.print_exc() 