
import os
import re

# Files to scan for tables
files = [
    'covering-papers.html', 'colored-boards.html', 'white-cream.html', 'kraft.html', 
    'black-recycled.html', 'textures.html', 'recycled-papers.html', 
    'premium-print.html', 'textured-finish.html', 'coated-specialty.html'
]

def slugify(text):
    return text.lower().strip().replace(' ', '-') + '.html'

def process_file(filename):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find TRs in the body of the table
    # Looking for <tr> that contains a product name in the first td
    # This is a bit complex with regex, so we'll do a robust line-by-line or chunk approach
    
    # Strategy: Find <tr>...</tr> blocks. Check if inside there's a <td>...<strong>Product Name</strong>...</td>
    # If so, extract product name, build URL, and inject onclick.
    
    def replacer(match):
        tr_content = match.group(0)
        
        # Check if this TR already has onclick
        if 'onclick=' in tr_content:
            return tr_content

        # Find product name: <td data-label="Product"><strong>Name</strong></td>
        name_match = re.search(r'<td[^>]*data-label="Product"[^>]*>\s*<strong>(.*?)</strong>', tr_content, re.IGNORECASE)
        if not name_match:
            # Fallback for different formatting (maybe just td without strong)
            name_match = re.search(r'<td[^>]*data-label="Product"[^>]*>\s*(.*?)</td>', tr_content, re.IGNORECASE)
        
        if name_match:
            product_name = name_match.group(1).strip()
            # Clean up any inner HTML if present (like spans)
            product_name = re.sub(r'<[^>]+>', '', product_name)
            
            target_url = slugify(product_name)
            
            # Additional check: Does this target file exist?
            if os.path.exists(target_url):
                # Inject onclick and style
                new_open_tag = f'<tr onclick="window.location.href=\'{target_url}\'" style="cursor: pointer; transition: background 0.2s;" class="clickable-row">'
                return tr_content.replace('<tr>', new_open_tag, 1)
            else:
                 # Handle special mappings if file doesn't match slug
                 special_map = {
                     'raw black': 'shiro-echo-raw-black.html',
                     'classy covers': 'classy-covers.html'
                 }
                 if product_name.lower() in special_map and os.path.exists(special_map[product_name.lower()]):
                     target_url = special_map[product_name.lower()]
                     new_open_tag = f'<tr onclick="window.location.href=\'{target_url}\'" style="cursor: pointer; transition: background 0.2s;" class="clickable-row">'
                     return tr_content.replace('<tr>', new_open_tag, 1)
        
        return tr_content

    # Regex to capture TR blocks. 
    # Use dotall to match across lines. Non-greedy.
    new_content = re.sub(r'<tr.*?>.*?</tr>', replacer, content, flags=re.DOTALL | re.IGNORECASE)
    
    if new_content != content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"No changes for {filename}")

for f in files:
    process_file(f)

print("Table rows updated.")
