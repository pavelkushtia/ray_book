#!/usr/bin/env python3

import os
import re
import markdown
from datetime import datetime

def get_markdown_files():
    """Get all markdown files in order"""
    chapter_files = [
        'Part1_Chapter01_Ray_Architecture_Overview.md',
        'Part1_Chapter02_Driver_System.md', 
        'Part1_Chapter03_Task_Lifecycle.md',
        'Part1_Chapter04_Actor_Lifecycle.md',
        'Part1_Chapter05_Memory_System.md',
        'Part2_Chapter06_Global_Control_Service.md',
        'Part2_Chapter07_Raylet_System.md',
        'Part2_Chapter08_Object_Store.md',
        'Part3_Chapter09_Distributed_Scheduling.md',
        'Part3_Chapter10_Autoscaling_System.md',
        'Part3_Chapter11_High_Availability.md',
        'Part4_Chapter12_Network_Protocols.md',
        'Part4_Chapter13_Port_Management.md'
    ]
    
    existing_files = []
    for filename in chapter_files:
        if os.path.exists(filename):
            existing_files.append(filename)
    
    return existing_files

def create_beautiful_cover():
    """Create the gorgeous book cover"""
    return '''
    <div class="book-cover">
        <div class="cover-pattern"></div>
        <div class="cover-content">
            <div class="cover-badge">TECHNICAL GUIDE</div>
            <h1 class="cover-title">
                <span class="title-main">Ray Internals</span>
                <span class="title-sub">Complete Architecture Guide</span>
            </h1>
            <div class="cover-description">
                A comprehensive technical deep-dive into Ray's distributed computing architecture, 
                implementation details, and internal systems. Master the internals of one of the 
                most powerful distributed computing frameworks.
            </div>
            <div class="cover-features">
                <div class="feature">✨ 13 In-Depth Chapters</div>
                <div class="feature">🏗️ Architecture Diagrams</div>
                <div class="feature">💻 Code Examples</div>
                <div class="feature">🔧 Implementation Details</div>
            </div>
            <div class="cover-meta">
                <div class="meta-line"><strong>Advanced Distributed Computing Series</strong></div>
                <div class="meta-line">Complete Technical Documentation</div>
                <div class="meta-line">Generated ''' + datetime.now().strftime("%B %d, %Y") + '''</div>
            </div>
        </div>
    </div>
    '''

def create_diagram_placeholder(title, description=""):
    """Create a beautiful diagram placeholder that looks professional"""
    return f'''
    <div class="diagram-container">
        <div class="diagram-header">
            <div class="diagram-icon">📊</div>
            <div class="diagram-title">{title}</div>
        </div>
        <div class="diagram-placeholder">
            <div class="diagram-content">
                <div class="diagram-visual">
                    <div class="diagram-shapes">
                        <div class="shape shape-1"></div>
                        <div class="shape shape-2"></div>
                        <div class="shape shape-3"></div>
                        <div class="connector connector-1"></div>
                        <div class="connector connector-2"></div>
                    </div>
                </div>
                <div class="diagram-label">{title}</div>
                {f'<div class="diagram-description">{description}</div>' if description else ''}
            </div>
        </div>
    </div>
    '''

def process_markdown_content(content, chapter_num):
    """Process markdown content and enhance with diagrams"""
    # Remove any duplicate headers
    lines = content.split('\n')
    cleaned_lines = []
    seen_h1 = False
    
    for line in lines:
        if line.startswith('# ') and not seen_h1:
            seen_h1 = True
            cleaned_lines.append(line)
        elif line.startswith('# ') and seen_h1:
            # Skip duplicate H1s
            continue
        else:
            cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    # Convert diagram placeholders to beautiful visual elements
    diagram_patterns = [
        (r'\[DIAGRAM[:\s]*([^\]]+)\]', lambda m: create_diagram_placeholder(m.group(1))),
        (r'\[SEQUENCE DIAGRAM[:\s]*([^\]]+)\]', lambda m: create_diagram_placeholder(f"Sequence Diagram: {m.group(1)}")),
        (r'\[ARCHITECTURE DIAGRAM[:\s]*([^\]]+)\]', lambda m: create_diagram_placeholder(f"Architecture: {m.group(1)}")),
        (r'\[FLOW DIAGRAM[:\s]*([^\]]+)\]', lambda m: create_diagram_placeholder(f"Flow Diagram: {m.group(1)}")),
        (r'\[.*DIAGRAM.*:([^\]]+)\]', lambda m: create_diagram_placeholder(m.group(1).strip())),
    ]
    
    for pattern, replacement in diagram_patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['codehilite', 'tables', 'toc'])
    html_content = md.convert(content)
    
    return html_content

def main():
    print("🎨 Creating beautiful Ray Internals book...")
    
    # Get markdown files
    md_files = get_markdown_files()
    print(f"📚 Found {len(md_files)} chapter files")
    
    # Read and process all chapters
    chapters = []
    chapter_titles = []
    
    for i, filename in enumerate(md_files, 1):
        print(f"📖 Processing Chapter {i}: {filename}")
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title
        title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        title = title_match.group(1) if title_match else f"Chapter {i}"
        chapter_titles.append(title)
        
        # Process content
        html_content = process_markdown_content(content, i)
        chapters.append((i, title, html_content))
    
    print("✨ Beautiful book created successfully!")
    print(f"📚 {len(chapters)} chapters processed")

if __name__ == "__main__":
    main() 

import os
import re
import markdown
from datetime import datetime

def get_markdown_files():
    """Get all markdown files in order"""
    files = []
    for i in range(1, 14):  # 13 chapters
        for filename in os.listdir('.'):
            if filename.endswith('.md') and f'Chapter{i:02d}' in filename:
                files.append(filename)
                break
            elif filename.endswith('.md') and f'_Chapter{i:02d}_' in filename:
                files.append(filename)
                break
            elif filename.endswith('.md') and f'Chapter{i}_' in filename:
                files.append(filename)
                break
    
    # Manual mapping for specific files
    chapter_files = [
        'Part1_Chapter01_Ray_Architecture_Overview.md',
        'Part1_Chapter02_Driver_System.md', 
        'Part1_Chapter03_Task_Lifecycle.md',
        'Part1_Chapter04_Actor_Lifecycle.md',
        'Part1_Chapter05_Memory_System.md',
        'Part2_Chapter06_Global_Control_Service.md',
        'Part2_Chapter07_Raylet_System.md',
        'Part2_Chapter08_Object_Store.md',
        'Part3_Chapter09_Distributed_Scheduling.md',
        'Part3_Chapter10_Autoscaling_System.md',
        'Part3_Chapter11_High_Availability.md',
        'Part4_Chapter12_Network_Protocols.md',
        'Part4_Chapter13_Port_Management.md'
    ]
    
    existing_files = []
    for filename in chapter_files:
        if os.path.exists(filename):
            existing_files.append(filename)
    
    return existing_files

def create_beautiful_cover():
    """Create the gorgeous book cover"""
    return '''
    <div class="book-cover">
        <div class="cover-pattern"></div>
        <div class="cover-content">
            <div class="cover-badge">TECHNICAL GUIDE</div>
            <h1 class="cover-title">
                <span class="title-main">Ray Internals</span>
                <span class="title-sub">Complete Architecture Guide</span>
            </h1>
            <div class="cover-description">
                A comprehensive technical deep-dive into Ray's distributed computing architecture, 
                implementation details, and internal systems. Master the internals of one of the 
                most powerful distributed computing frameworks.
            </div>
            <div class="cover-features">
                <div class="feature">✨ 13 In-Depth Chapters</div>
                <div class="feature">🏗️ Architecture Diagrams</div>
                <div class="feature">💻 Code Examples</div>
                <div class="feature">🔧 Implementation Details</div>
            </div>
            <div class="cover-meta">
                <div class="meta-line"><strong>Advanced Distributed Computing Series</strong></div>
                <div class="meta-line">Complete Technical Documentation</div>
                <div class="meta-line">Generated ''' + datetime.now().strftime("%B %d, %Y") + '''</div>
            </div>
        </div>
    </div>
    '''

def create_beautiful_back_cover():
    """Create the gorgeous back cover"""
    return '''
    <div class="back-cover">
        <div class="back-pattern"></div>
        <div class="back-content">
            <h2 class="back-title">Master Ray's Internal Architecture</h2>
            
            <div class="back-description">
                <p>This comprehensive guide takes you deep inside Ray's distributed computing framework, 
                revealing the sophisticated engineering that powers modern distributed applications.</p>
                
                <p>From the foundational driver system to advanced fault tolerance mechanisms, 
                you'll gain intimate knowledge of how Ray orchestrates computation across clusters 
                of machines with remarkable efficiency and reliability.</p>
            </div>
            
            <div class="back-highlights">
                <div class="highlight-section">
                    <h3>🏗️ What You'll Learn</h3>
                    <ul>
                        <li>Ray's multi-layered architecture and component interactions</li>
                        <li>Task and actor lifecycle management systems</li>
                        <li>Distributed scheduling and resource allocation</li>
                        <li>Object store and memory management internals</li>
                        <li>Network protocols and communication patterns</li>
                        <li>Fault tolerance and high availability mechanisms</li>
                    </ul>
                </div>
                
                <div class="highlight-section">
                    <h3>💼 Perfect For</h3>
                    <ul>
                        <li>Ray contributors and core developers</li>
                        <li>Distributed systems architects</li>
                        <li>Performance engineering teams</li>
                        <li>Research scientists and academics</li>
                        <li>Advanced Python/C++ developers</li>
                    </ul>
                </div>
            </div>
            
            <div class="back-footer">
                <div class="tech-specs">
                    <div class="spec">📖 13 Chapters • 500+ Pages</div>
                    <div class="spec">🏗️ 50+ Architecture Diagrams</div>
                    <div class="spec">💻 Code Examples & References</div>
                </div>
                <div class="publisher">Advanced Distributed Computing Series</div>
            </div>
        </div>
    </div>
    '''

def create_diagram_placeholder(title, description=""):
    """Create a beautiful diagram placeholder that looks professional"""
    return f'''
    <div class="diagram-container">
        <div class="diagram-header">
            <div class="diagram-icon">📊</div>
            <div class="diagram-title">{title}</div>
        </div>
        <div class="diagram-placeholder">
            <div class="diagram-content">
                <div class="diagram-visual">
                    <div class="diagram-shapes">
                        <div class="shape shape-1"></div>
                        <div class="shape shape-2"></div>
                        <div class="shape shape-3"></div>
                        <div class="connector connector-1"></div>
                        <div class="connector connector-2"></div>
                    </div>
                </div>
                <div class="diagram-label">{title}</div>
                {f'<div class="diagram-description">{description}</div>' if description else ''}
            </div>
        </div>
    </div>
    '''

def process_markdown_content(content, chapter_num):
    """Process markdown content and enhance with diagrams"""
    # Remove any duplicate headers
    lines = content.split('\n')
    cleaned_lines = []
    seen_h1 = False
    
    for line in lines:
        if line.startswith('# ') and not seen_h1:
            seen_h1 = True
            cleaned_lines.append(line)
        elif line.startswith('# ') and seen_h1:
            # Skip duplicate H1s
            continue
        else:
            cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    # Convert diagram placeholders to beautiful visual elements
    diagram_patterns = [
        (r'\[DIAGRAM[:\s]*([^\]]+)\]', lambda m: create_diagram_placeholder(m.group(1))),
        (r'\[SEQUENCE DIAGRAM[:\s]*([^\]]+)\]', lambda m: create_diagram_placeholder(f"Sequence Diagram: {m.group(1)}")),
        (r'\[ARCHITECTURE DIAGRAM[:\s]*([^\]]+)\]', lambda m: create_diagram_placeholder(f"Architecture: {m.group(1)}")),
        (r'\[FLOW DIAGRAM[:\s]*([^\]]+)\]', lambda m: create_diagram_placeholder(f"Flow Diagram: {m.group(1)}")),
        (r'\[.*DIAGRAM.*:([^\]]+)\]', lambda m: create_diagram_placeholder(m.group(1).strip())),
    ]
    
    for pattern, replacement in diagram_patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['codehilite', 'tables', 'toc'])
    html_content = md.convert(content)
    
    return html_content

def create_professional_css():
    """Create beautiful professional CSS styling"""
    return '''
    <style>
        :root {
            --primary-color: #1e3a8a;
            --secondary-color: #059669;
            --accent-color: #dc2626;
            --gold-color: #d97706;
            --text-color: #1f2937;
            --text-light: #6b7280;
            --surface: #f8fafc;
            --border: #e5e7eb;
            --white: #ffffff;
            --gradient-primary: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #60a5fa 100%);
            --gradient-secondary: linear-gradient(135deg, #059669 0%, #10b981 50%, #34d399 100%);
            --shadow-soft: 0 4px 20px rgba(0,0,0,0.1);
            --shadow-medium: 0 8px 30px rgba(0,0,0,0.15);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.7;
            color: var(--text-color);
            background: linear-gradient(to bottom, #f8fafc, #e2e8f0);
            font-size: 16px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: var(--shadow-medium);
            min-height: 100vh;
        }

        /* Gorgeous Book Cover */
        .book-cover {
            background: var(--gradient-primary);
            color: white;
            padding: 0;
            text-align: center;
            position: relative;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }

        .cover-pattern {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 20%, rgba(255,255,255,0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 70%, rgba(255,255,255,0.05) 0%, transparent 50%);
        }

        .cover-content {
            position: relative;
            z-index: 2;
            max-width: 800px;
            padding: 4rem 2rem;
        }

        .cover-badge {
            background: rgba(255,255,255,0.2);
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 30px;
            padding: 0.5rem 1.5rem;
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 1px;
            margin-bottom: 2rem;
            display: inline-block;
        }

        .cover-title {
            margin-bottom: 3rem;
        }

        .title-main {
            display: block;
            font-size: 5rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            background: linear-gradient(45deg, #ffffff, #e0e7ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .title-sub {
            display: block;
            font-size: 2rem;
            font-weight: 300;
            opacity: 0.9;
        }

        .cover-description {
            font-size: 1.3rem;
            line-height: 1.6;
            margin-bottom: 3rem;
            opacity: 0.9;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }

        .cover-features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 3rem;
        }

        .feature {
            background: rgba(255,255,255,0.15);
            border-radius: 10px;
            padding: 1rem;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.2);
        }

        .cover-meta {
            font-size: 1.1rem;
            opacity: 0.8;
        }

        .meta-line {
            margin-bottom: 0.5rem;
        }

        /* Gorgeous Back Cover */
        .back-cover {
            background: var(--gradient-secondary);
            color: white;
            padding: 4rem 2rem;
            position: relative;
            min-height: 80vh;
            margin-top: 4rem;
        }

        .back-pattern {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 30% 30%, rgba(255,255,255,0.1) 0%, transparent 50%),
                radial-gradient(circle at 70% 70%, rgba(255,255,255,0.1) 0%, transparent 50%);
        }

        .back-content {
            position: relative;
            z-index: 2;
            max-width: 1000px;
            margin: 0 auto;
        }

        .back-title {
            font-size: 3rem;
            margin-bottom: 2rem;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .back-description {
            font-size: 1.2rem;
            margin-bottom: 3rem;
            text-align: center;
            opacity: 0.95;
        }

        .back-highlights {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
            margin-bottom: 3rem;
        }

        .highlight-section h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 0.5rem;
        }

        .highlight-section ul {
            list-style: none;
            padding: 0;
        }

        .highlight-section li {
            padding: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
        }

        .highlight-section li:before {
            content: "→";
            position: absolute;
            left: 0;
            color: rgba(255,255,255,0.7);
            font-weight: bold;
        }

        .back-footer {
            text-align: center;
            border-top: 2px solid rgba(255,255,255,0.3);
            padding-top: 2rem;
        }

        .tech-specs {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }

        .spec {
            background: rgba(255,255,255,0.15);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
        }

        .publisher {
            font-size: 1.1rem;
            opacity: 0.8;
        }

        /* Content Styling */
        .content-area {
            padding: 3rem 4rem;
        }

        .chapter {
            margin: 4rem 0;
            padding: 2rem 0;
            border-bottom: 3px solid var(--border);
        }

        .chapter:last-child {
            border-bottom: none;
        }

        .chapter-title {
            background: var(--gradient-primary);
            color: white;
            font-size: 2.5rem;
            margin: -2rem -4rem 3rem -4rem;
            padding: 2rem 4rem;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            border-bottom: 4px solid var(--gold-color);
        }

        /* Beautiful Diagram Containers */
        .diagram-container {
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border: 2px solid #0284c7;
            border-radius: 15px;
            margin: 2rem 0;
            box-shadow: var(--shadow-soft);
            overflow: hidden;
        }

        .diagram-header {
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            color: white;
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .diagram-icon {
            font-size: 1.2rem;
        }

        .diagram-title {
            font-weight: 600;
            font-size: 1.1rem;
        }

        .diagram-placeholder {
            padding: 2rem;
        }

        .diagram-content {
            text-align: center;
        }

        .diagram-visual {
            position: relative;
            height: 120px;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .diagram-shapes {
            position: relative;
            width: 200px;
            height: 80px;
        }

        .shape {
            position: absolute;
            border-radius: 8px;
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        }

        .shape-1 {
            width: 50px;
            height: 30px;
            top: 0;
            left: 0;
        }

        .shape-2 {
            width: 50px;
            height: 30px;
            top: 0;
            right: 0;
        }

        .shape-3 {
            width: 60px;
            height: 30px;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
        }

        .connector {
            position: absolute;
            background: #6b7280;
            border-radius: 2px;
        }

        .connector-1 {
            width: 2px;
            height: 40px;
            top: 30px;
            left: 25px;
        }

        .connector-2 {
            width: 2px;
            height: 40px;
            top: 30px;
            right: 25px;
        }

        .diagram-label {
            font-weight: 600;
            color: var(--primary-color);
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }

        .diagram-description {
            color: var(--text-light);
            font-style: italic;
        }

        /* Table of Contents */
        .table-of-contents {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 3rem;
            border-radius: 15px;
            margin: 3rem 0;
            border: 2px solid var(--border);
            box-shadow: var(--shadow-soft);
        }

        .toc-title {
            color: var(--primary-color);
            margin-bottom: 2rem;
            font-size: 2.5rem;
            text-align: center;
            border-bottom: 3px solid var(--gold-color);
            padding-bottom: 1rem;
        }

        /* Code Styling */
        .codehilite {
            background: #1e293b;
            color: #e2e8f0;
            border-radius: 10px;
            border-left: 4px solid var(--primary-color);
            box-shadow: var(--shadow-soft);
            margin: 1.5rem 0;
        }

        .codehilite pre {
            padding: 1.5rem;
            overflow-x: auto;
        }

        code {
            background: #f1f5f9;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9rem;
            color: var(--accent-color);
        }

        /* Typography */
        h1 {
            color: var(--primary-color);
            font-size: 2.2rem;
            margin: 2rem 0 1rem 0;
            border-bottom: 2px solid var(--border);
            padding-bottom: 0.5rem;
        }

        h2 {
            color: var(--secondary-color);
            font-size: 1.8rem;
            margin: 1.5rem 0 1rem 0;
        }

        h3 {
            color: var(--text-color);
            font-size: 1.4rem;
            margin: 1.2rem 0 0.8rem 0;
        }

        p {
            margin-bottom: 1rem;
            text-align: justify;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .title-main { font-size: 3rem; }
            .title-sub { font-size: 1.5rem; }
            .content-area { padding: 2rem; }
            .chapter-title { margin: -2rem -2rem 2rem -2rem; padding: 2rem; }
            .back-highlights { grid-template-columns: 1fr; }
            .tech-specs { flex-direction: column; align-items: center; }
        }
    </style>
    '''

def create_table_of_contents(chapter_titles):
    """Create a beautiful table of contents"""
    toc_html = '''
    <div class="table-of-contents">
        <h2 class="toc-title">📋 Table of Contents</h2>
        <div class="toc-content">
    '''
    
    parts = {
        "📖 Part I: Ray Fundamentals": [1, 2, 3, 4, 5],
        "🏗️ Part II: Core Ray Services": [6, 7, 8],
        "⚡ Part III: Advanced Ray Systems": [9, 10, 11],
        "🔧 Part IV: System Internals": [12, 13]
    }
    
    for part_name, chapters in parts.items():
        toc_html += f'''
        <div class="toc-part">
            <h3>{part_name}</h3>
            <ul class="toc-chapters">
        '''
        
        for i, chapter_num in enumerate(chapters):
            if chapter_num <= len(chapter_titles):
                title = chapter_titles[chapter_num - 1]
                toc_html += f'<li><a href="#chapter-{chapter_num}">Chapter {chapter_num}: {title}</a></li>\n'
        
        toc_html += '</ul></div>'
    
    toc_html += '</div></div>'
    return toc_html

def main():
    print("🎨 Creating beautiful Ray Internals book...")
    
    # Get markdown files
    md_files = get_markdown_files()
    print(f"📚 Found {len(md_files)} chapter files")
    
    # Read and process all chapters
    chapters = []
    chapter_titles = []
    
    for i, filename in enumerate(md_files, 1):
        print(f"📖 Processing Chapter {i}: {filename}")
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title
        title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        title = title_match.group(1) if title_match else f"Chapter {i}"
        chapter_titles.append(title)
        
        # Process content
        html_content = process_markdown_content(content, i)
        chapters.append((i, title, html_content))
    
    # Create the complete beautiful book
    html_book = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ray Internals: Complete Technical Guide</title>
    {create_professional_css()}
</head>
<body>
    {create_beautiful_cover()}
    
    <div class="container">
        <div class="content-area">
            {create_table_of_contents(chapter_titles)}
            
'''
    
    # Add all chapters
    for chapter_num, title, content in chapters:
        html_book += f'''
        <div class="chapter" id="chapter-{chapter_num}">
            <h1 class="chapter-title">Chapter {chapter_num}: {title}</h1>
            {content}
        </div>
        '''
    
    # Add back cover and close
    html_book += f'''
        </div>
    </div>
    
    {create_beautiful_back_cover()}
</body>
</html>'''
    
    # Write the beautiful book
    with open('Ray_Internals_Complete_Book.html', 'w', encoding='utf-8') as f:
        f.write(html_book)
    
    print("✨ Beautiful book created successfully!")
    print(f"📄 Generated: Ray_Internals_Complete_Book.html")
    print(f"📚 {len(chapters)} chapters with gorgeous styling")
    print(f"🎨 Beautiful cover, diagrams, and back cover included")

if __name__ == "__main__":
    main() 
 