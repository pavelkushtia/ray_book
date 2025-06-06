#!/usr/bin/env python3
"""
Simple PDF creator using system print functionality
"""

import os
import subprocess
import webbrowser
import tempfile
import time

def create_pdf_via_browser():
    """Create PDF by opening HTML in browser for user to print"""
    html_file = "Ray_Internals_PDF_Ready.html"
    
    if not os.path.exists(html_file):
        print("❌ HTML file not found:", html_file)
        return False
    
    # Get absolute path
    abs_path = os.path.abspath(html_file)
    file_url = f"file://{abs_path}"
    
    print("🌐 Opening HTML file in your default browser...")
    print(f"📄 File: {abs_path}")
    
    try:
        webbrowser.open(file_url)
        print("\n🎯 NEXT STEPS:")
        print("1. ⏳ Wait for the page to load completely (5-10 seconds)")
        print("2. 🖨️ Press Ctrl+P (or Cmd+P on Mac)")
        print("3. 📄 Choose 'Save as PDF' as destination")
        print("4. ⚙️ Settings:")
        print("   - Paper size: A4")
        print("   - Margins: Default")
        print("   - Scale: 100%")
        print("   - Headers/footers: Yes")
        print("   - Background graphics: Yes")
        print("5. 💾 Save as: Ray_Internals_Complete_Guide.pdf")
        print("\n✅ This will create your professional PDF with all diagrams!")
        return True
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        return False

def check_pdf_exists():
    """Check if PDF was created"""
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    if pdf_files:
        print(f"\n🎉 PDF files found: {', '.join(pdf_files)}")
        for pdf in pdf_files:
            size = os.path.getsize(pdf) / (1024*1024)
            print(f"📊 {pdf}: {size:.2f} MB")
    else:
        print("\n❓ No PDF files found yet. Follow the browser instructions above.")

if __name__ == "__main__":
    print("🚀 Ray Internals PDF Creator")
    print("=" * 50)
    
    success = create_pdf_via_browser()
    
    if success:
        print("\n⌚ Waiting 10 seconds for you to start the process...")
        time.sleep(10)
        check_pdf_exists()
        
        print("\n📋 Alternative Method (if browser doesn't work):")
        print("1. Right-click on Ray_Internals_PDF_Ready.html")
        print("2. Choose 'Open with Browser'") 
        print("3. Follow the print-to-PDF steps above")
    else:
        print("❌ Failed to open browser automatically")
        print("📋 Manual steps:")
        print("1. Double-click Ray_Internals_PDF_Ready.html")
        print("2. Wait for page to load")
        print("3. Press Ctrl+P and save as PDF") 