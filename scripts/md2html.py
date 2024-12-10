#!/usr/bin/env python3
import sys
import markdown
import argparse
from pygments.formatters import HtmlFormatter

# Script written by Claude, of course :~)

def get_pygments_css():
    """Get the default Pygments CSS."""
    return HtmlFormatter().get_style_defs('.codehilite')

def convert_markdown_to_html(input_file, output_file=None):
    """
    Convert a markdown file to HTML with support for code blocks and raw HTML.

    Args:
        input_file (str): Path to input markdown file
        output_file (str, optional): Path to output HTML file. If None, derives from input name
    """
    # If no output file specified, replace .md with .html
    if not output_file:
        output_file = input_file.rsplit('.', 1)[0] + '.html'

    # Read markdown content
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert to HTML using Python-Markdown
    html_content = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'codehilite', 'tables']
    )

    # Get Pygments CSS
    pygments_css = get_pygments_css()

    # Basic HTML template with styling
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{input_file}</title>
    <style>
        /* Pygments Syntax Highlighting */
        {pygments_css}

        /* Basic reset and fonts */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            padding: 2rem 1rem;
            background-color: #f8f9fa;
        }}

        /* Center column layout */
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 2rem 3rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        /* Typography */
        h1 {{
            font-size: 2.2rem;
            margin-bottom: 1.5rem;
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 0.5rem;
        }}

        h2 {{
            font-size: 1.8rem;
            margin: 2rem 0 1rem;
            color: #34495e;
        }}

        p {{
            margin-bottom: 1rem;
        }}

        /* Code blocks */
        .codehilite {{
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 1rem;
            overflow-x: auto;
            margin: 1rem 0;
            border: 1px solid #e1e4e8;
        }}

        code {{
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.9em;
            padding: 0.2em 0.4em;
            background-color: #f6f8fa;
            border-radius: 3px;
        }}

        .codehilite code {{
            padding: 0;
            background-color: transparent;
        }}

        /* Links */
        a {{
            color: #0366d6;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>
"""

    # Write the HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

    return output_file

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown files to HTML')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('-o', '--output', help='Output HTML file (optional)')
    args = parser.parse_args()

    output_file = convert_markdown_to_html(args.input, args.output)
    print(f"Converted {args.input} to {output_file}")

if __name__ == '__main__':
    main()
