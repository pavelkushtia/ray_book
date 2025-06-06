#!/usr/bin/env python3
"""
EPUB to PDF Converter

This script converts the Ray Internals EPUB e-book to a PDF with proper formatting.
"""

import zipfile
import os
import re
from xml.etree import ElementTree as ET
import datetime

def extract_epub_content(epub_path):
    """Extract content from EPUB file."""
    print(f"📖 Extracting content from {epub_path}...")
    
    chapters = []
    
    try:
        with zipfile.ZipFile(epub_path, 'r') as epub:
            # Read the content.opf to get chapter order
            opf_content = epub.read('OEBPS/content.opf').decode('utf-8')
            
            # Parse OPF to get spine order
            root = ET.fromstring(opf_content)
            ns = {'opf': 'http://www.idpf.org/2007/opf'}
            
            spine_items = []
            for itemref in root.findall('.//opf:spine/opf:itemref', ns):
                idref = itemref.get('idref')
                spine_items.append(idref)
            
            # Get manifest items
            manifest_items = {}
            for item in root.findall('.//opf:manifest/opf:item', ns):
                item_id = item.get('id')
                href = item.get('href')
                if href.endswith('.xhtml'):
                    manifest_items[item_id] = href
            
            # Extract chapters in spine order
            for item_id in spine_items:
                if item_id in manifest_items:
                    chapter_file = f"OEBPS/{manifest_items[item_id]}"
                    try:
                        chapter_content = epub.read(chapter_file).decode('utf-8')
                        # Extract title and body content
                        title_match = re.search(r'<title>(.*?)</title>', chapter_content)
                        title = title_match.group(1) if title_match else f"Chapter {len(chapters)+1}"
                        
                        # Extract body content
                        body_match = re.search(r'<body>(.*?)</body>', chapter_content, re.DOTALL)
                        body_content = body_match.group(1) if body_match else chapter_content
                        
                        chapters.append((title, body_content))
                        print(f"  ✓ Extracted: {title}")
                    except Exception as e:
                        print(f"  ⚠ Warning: Could not read {chapter_file}: {e}")
            
    except Exception as e:
        print(f"❌ Error reading EPUB file: {e}")
        return []
    
    return chapters

def html_to_text_with_formatting(html_content):
    """Convert HTML content to formatted text suitable for PDF generation."""
    # Remove XML/HTML tags but preserve structure
    content = html_content
    
    # Convert headers to text with proper spacing
    content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n\n# \1\n' + '='*60 + '\n', content, flags=re.DOTALL)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n\n## \1\n' + '-'*40 + '\n', content, flags=re.DOTALL)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n\n### \1\n', content, flags=re.DOTALL)
    content = re.sub(r'<h[4-6][^>]*>(.*?)</h[4-6]>', r'\n\n#### \1\n', content, flags=re.DOTALL)
    
    # Convert paragraphs
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\1\n', content, flags=re.DOTALL)
    
    # Convert code blocks
    content = re.sub(r'<pre[^>]*>(.*?)</pre>', r'\n```\n\1\n```\n', content, flags=re.DOTALL)
    content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.DOTALL)
    
    # Convert lists
    content = re.sub(r'<ul[^>]*>(.*?)</ul>', r'\n\1\n', content, flags=re.DOTALL)
    content = re.sub(r'<ol[^>]*>(.*?)</ol>', r'\n\1\n', content, flags=re.DOTALL)
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'  • \1\n', content, flags=re.DOTALL)
    
    # Convert blockquotes
    content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'\n> \1\n', content, flags=re.DOTALL)
    
    # Convert tables (simplified)
    content = re.sub(r'<table[^>]*>(.*?)</table>', r'\n[TABLE]\n\1\n[/TABLE]\n', content, flags=re.DOTALL)
    content = re.sub(r'<tr[^>]*>(.*?)</tr>', r'\n| \1 |', content, flags=re.DOTALL)
    content = re.sub(r'<t[hd][^>]*>(.*?)</t[hd]>', r' \1 |', content, flags=re.DOTALL)
    
    # Remove remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Clean up whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    content = re.sub(r'^\s+', '', content, flags=re.MULTILINE)
    
    return content.strip()

def create_pdf_with_text(chapters, output_file):
    """Create PDF using simple text formatting (fallback method)."""
    print("🎨 Creating PDF with text formatting...")
    
    # Create a simple HTML file with good print CSS
    current_date = datetime.datetime.now().strftime("%B %Y")
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Ray Internals: A Comprehensive Technical Guide</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        
        body {{
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            color: #000;
            font-size: 12pt;
        }}
        
        h1 {{
            color: #1976d2;
            font-size: 18pt;
            margin: 30pt 0 15pt 0;
            border-bottom: 2pt solid #1976d2;
            padding-bottom: 5pt;
            page-break-after: avoid;
        }}
        
        h2 {{
            color: #388e3c;
            font-size: 14pt;
            margin: 20pt 0 10pt 0;
            page-break-after: avoid;
        }}
        
        h3 {{
            color: #f57c00;
            font-size: 12pt;
            margin: 15pt 0 8pt 0;
            page-break-after: avoid;
        }}
        
        h4 {{
            color: #c2185b;
            font-size: 11pt;
            margin: 12pt 0 6pt 0;
            page-break-after: avoid;
        }}
        
        p {{
            margin: 8pt 0;
            text-align: justify;
        }}
        
        pre, code {{
            font-family: 'Courier New', monospace;
            background-color: #f5f5f5;
            border: 1pt solid #ddd;
            padding: 8pt;
            margin: 8pt 0;
            font-size: 9pt;
            page-break-inside: avoid;
        }}
        
        code {{
            padding: 2pt 4pt;
            display: inline;
        }}
        
        .page-break {{
            page-break-before: always;
        }}
        
        .title-page {{
            text-align: center;
            margin-top: 100pt;
            page-break-after: always;
        }}
        
        .title-page h1 {{
            font-size: 24pt;
            border: none;
            margin-bottom: 20pt;
        }}
        
        .chapter-title {{
            page-break-before: always;
        }}
    </style>
</head>
<body>

<div class="title-page">
    <h1>Ray Internals</h1>
    <h2>A Comprehensive Technical Guide</h2>
    <p style="font-size: 14pt; color: #666; margin-top: 20pt;">
        The Complete Guide to Understanding Ray's Architecture, Implementation, and Internals
    </p>
    <p style="margin-top: 40pt; color: #888;">Generated: {current_date}</p>
</div>

"""
    
    for i, (title, content) in enumerate(chapters):
        if i > 0:
            html_content += '<div class="page-break"></div>\n'
        
        # Convert content to HTML
        text_content = html_to_text_with_formatting(content)
        
        # Convert back to HTML with proper formatting
        html_chapter = text_content
        html_chapter = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_chapter, flags=re.MULTILINE)
        html_chapter = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_chapter, flags=re.MULTILINE)
        html_chapter = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_chapter, flags=re.MULTILINE)
        html_chapter = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_chapter, flags=re.MULTILINE)
        
        # Convert code blocks
        html_chapter = re.sub(r'```\n(.*?)\n```', r'<pre><code>\1</code></pre>', html_chapter, flags=re.DOTALL)
        html_chapter = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_chapter)
        
        # Convert paragraphs
        lines = html_chapter.split('\n')
        formatted_lines = []
        in_pre = False
        
        for line in lines:
            if '<pre>' in line:
                in_pre = True
            elif '</pre>' in line:
                in_pre = False
            elif not in_pre and line.strip() and not line.startswith('<h') and not line.startswith('  •'):
                if not any(tag in line for tag in ['<code>', '<pre>', '<h1>', '<h2>', '<h3>', '<h4>']):
                    line = f'<p>{line}</p>'
            formatted_lines.append(line)
        
        html_chapter = '\n'.join(formatted_lines)
        
        html_content += html_chapter + '\n\n'
    
    html_content += """
</body>
</html>
"""
    
    # Write HTML file
    html_output = output_file.replace('.pdf', '.html')
    with open(html_output, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Created HTML file: {html_output}")
    print("💡 To convert to PDF:")
    print("  1. Open the HTML file in Chrome or Firefox")
    print("  2. Press Ctrl+P (Cmd+P on Mac)")
    print("  3. Select 'Save as PDF'")
    print("  4. Enable 'Background graphics' in More settings")
    print("  5. Save as PDF")
    
    return html_output

def convert_epub_to_pdf(epub_path, pdf_path):
    """Convert EPUB to PDF."""
    print(f"🚀 Converting {epub_path} to PDF...")
    
    # Extract content from EPUB
    chapters = extract_epub_content(epub_path)
    
    if not chapters:
        print("❌ No chapters found in EPUB file")
        return None
    
    print(f"📚 Found {len(chapters)} chapters")
    
    # Create PDF
    output_file = create_pdf_with_text(chapters, pdf_path)
    
    return output_file

if __name__ == "__main__":
    epub_file = "Ray_Internals_Complete_Guide.epub"
    pdf_file = "Ray_Internals_Complete_Guide_from_EPUB.pdf"
    
    if not os.path.exists(epub_file):
        print(f"❌ EPUB file not found: {epub_file}")
        print("Please make sure the EPUB file exists in the current directory.")
    else:
        try:
            result = convert_epub_to_pdf(epub_file, pdf_file)
            if result:
                print(f"\n🎉 Success! EPUB content converted to HTML: {result}")
                print("You can now print this HTML file to PDF using your browser.")
        except Exception as e:
            print(f"❌ Error during conversion: {str(e)}")
            import traceback
            traceback.print_exc() 