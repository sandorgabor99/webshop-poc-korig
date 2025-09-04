@echo off
echo ========================================
echo WebShop POC - PDF Converter
echo ========================================
echo.

REM Check if wkhtmltopdf is installed
where wkhtmltopdf >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing wkhtmltopdf...
    winget install --id wkhtmltopdf.wkhtmltopdf
    echo.
)

REM Create output directory
if not exist "pdf_docs" mkdir pdf_docs

echo Converting Markdown files to PDF...
echo.

REM Convert each markdown file
for %%f in (docs\*.md) do (
    echo Converting: %%~nxf
    python -c "
import markdown2
import os
from pathlib import Path

# Read markdown file
with open(r'%%f', 'r', encoding='utf-8') as f:
    content = f.read()

# Convert to HTML
html = markdown2.markdown(content, extras=['tables', 'fenced-code-blocks', 'code-friendly'])

# Create styled HTML
styled_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{Path(r'%%f').stem}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #7f8c8d; }}
        code {{ background-color: #f8f9fa; padding: 2px 4px; border-radius: 3px; font-family: 'Courier New', monospace; }}
        pre {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    {html}
</body>
</html>'''

# Save HTML file
html_file = f'pdf_docs/{Path(r"%%f").stem}.html'
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(styled_html)

print(f'HTML created: {html_file}')
"

    REM Convert HTML to PDF using wkhtmltopdf if available
    where wkhtmltopdf >nul 2>nul
    if %errorlevel% equ 0 (
        wkhtmltopdf --page-size A4 --margin-top 20 --margin-right 20 --margin-bottom 20 --margin-left 20 "pdf_docs\%%~nf.html" "pdf_docs\%%~nf.pdf"
        echo   PDF created: pdf_docs\%%~nf.pdf
    ) else (
        echo   HTML created: pdf_docs\%%~nf.html (use browser to print as PDF)
    )
    echo.
)

echo ========================================
echo Conversion Complete!
echo ========================================
echo.
echo Files created in 'pdf_docs' folder:
echo.
dir pdf_docs /b
echo.
echo To create PDFs from HTML files:
echo 1. Open HTML files in browser
echo 2. Press Ctrl+P to print
echo 3. Select 'Save as PDF'
echo.
pause
