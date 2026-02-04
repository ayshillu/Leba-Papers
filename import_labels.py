
import os
import re

# Source directory for mirrored files
SOURCE_DIR = 'products'
# Destination directory (root)
DEST_DIR = '.'

# Files to process (Labels)
LABEL_FILES = [
    'maplitho-paper-labels.html',
    'chromo-paper-labels.html',
    'highgloss-paper-labels.html',
    'castcoated-paper-labels.html',
    'fluorescent-paper-labels.html',
    'goldpaper-paper-labels.html',
    'metallised-paper-labels.html',
    'metallisedholographic-paper-labels.html',
    'pvcclear-film-labels.html',
    'synthetic-film-labels.html',
    'polyclear-film-labels.html',
    'polyopaque-film-labels.html',
    'polymetallised-film-labels.html',
    'pvcmetallised-film-labels.html',
    'removable-special-labels.html',
    'piggyback-special-labels.html',
    'ecofriendly-special-labels.html',
    'kraftpaper-special-labels.html',
    'blackpaper-special-labels.html',
    'sandwich-special-labels.html'
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | NVG Speciality Papers</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
</head>
<body>
    <!-- FLOATING NAV (DESKTOP) -->
    <nav class="nav-pill desktop-only">
        <div class="nav-item">
            <a href="index.html" class="nav-link">Home</a>
        </div>
        <div class="nav-item">
            <span class="nav-link">Graphic Speciality</span>
            <div class="dropdown-menu">
                <!-- Mega Menu Content injected by JS or server -->
            </div>
        </div>
        <div class="nav-item">
            <span class="nav-link">Labels</span>
             <div class="dropdown-menu">
                 <!-- Labels Menu content -->
             </div>
        </div>
        <div class="nav-item">
            <a href="applications.html" class="nav-link">Applications</a>
        </div>
         <div class="nav-item">
            <a href="capabilities.html" class="nav-link">Capacity</a>
        </div>
        <div class="nav-item">
             <a href="contact.html" class="btn btn-primary">Contact</a>
        </div>
    </nav>
    
    <!-- MOBILE NAV OVERLAY -->
    <!-- (Injected by update_site.py) -->

    <div class="main-wrapper" style="padding-top: 100px;">
        
        <!-- BANNER -->
        <section class="panel reveal-panel" style="padding-bottom: 20px;">
             <div class="container">
                <div class="grid grid-2" style="align-items: center;">
                    <div>
                        <span class="label">Labels</span>
                        <h1>{product_name}</h1>
                        <p>{description}</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- TABLE SECTION -->
        <section class="panel reveal-panel">
            <div class="container">
                {table_content}
            </div>
        </section>
        
        <!-- DOWNLOAD SECTION -->
        <section class="panel reveal-panel" style="background: #f8f9fa; margin-top: 40px;">
            <div class="container">
                 {download_content}
            </div>
        </section>

    </div>

    <!-- FOOTER -->
    <!-- (Injected by update_site.py) -->
    
    <script src="main.js"></script>
</body>
</html>
"""

def extract_content(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract Product Name from Banner
    # <h2>Maplitho</h2>
    name_match = re.search(r'<h2>(.*?)</h2>', content)
    product_name = name_match.group(1).strip() if name_match else "Product"
    
    # Extract Table
    # <div class="table-responsive">...</table></div>
    table_match = re.search(r'(<div class="table-responsive">.*?</table>\s*</div>)', content, re.DOTALL)
    table_content = table_match.group(1) if table_match else "<p>No specification table available.</p>"
    
    # Clean Table
    # Remove style attributes to let CSS handle it? Or keep bootstrap classes and map them?
    # Mirror uses 'table table-bordered table-striped'. My CSS might not have these.
    # I should add basic table styles to CSS if missing.
    
    # Extract Download Section
    # <div class="... download-pdf" ...>...</div>
    # Regex is tricky with nested divs. Let's look for known start and end markers.
    download_match = re.search(r'(<div[^>]*class="[^"]*download-pdf[^"]*"[^>]*>.*?</ul>\s*</div>)', content, re.DOTALL)
    download_content = download_match.group(1) if download_match else ""
    
    # Fix Image Paths in Download Content
    # images/download-pdf.png -> productimages/icons/download-pdf.png (Guessing location)
    # pdf/... -> productimages/pdf/... (Guessing)
    # Actually, mirror links to 'pdf/maplitho/...'. I need to make sure 'pdf' folder exists in root or productimages.
    
    if download_content:
        download_content = download_content.replace('images/download-pdf.png', 'productimages/icons/download-pdf.png') # Update this path if needed
        # Check pdf links.
    
    return {
        'product_name': product_name,
        'description': "Premium Label Solutions", # Mirror doesn't always have description in banner, sometimes in About.
        'table_content': table_content,
        'download_content': download_content
    }

def process_files():
    for f in LABEL_FILES:
        src_path = os.path.join(SOURCE_DIR, f)
        data = extract_content(src_path)
        
        if not data:
            continue
            
        # Create HTML
        html = TEMPLATE.format(
            title=data['product_name'],
            product_name=data['product_name'],
            description=data['description'],
            table_content=data['table_content'],
            download_content=data['download_content']
        )
        
        dest_path = os.path.join(DEST_DIR, f)
        with open(dest_path, 'w', encoding='utf-8') as f_out:
            f_out.write(html)
        print(f"Created {f}")

if __name__ == "__main__":
    process_files()
