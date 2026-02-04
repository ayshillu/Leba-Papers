
import os
import re

# Define the products data
products = [
    {'name': 'Buckram', 'cat': 'Covering', 'cat_page': 'covering-papers.html', 'size': '71x102, 76x102', 'gsm': '120', 'desc': 'Matt finish covering paper with high folding strength and durability.'},
    {'name': 'Glossy', 'cat': 'Covering', 'cat_page': 'covering-papers.html', 'size': '78.7x101.6, 72x102', 'gsm': '120', 'desc': 'Premium glossy finish covering papers for high-impact packaging.'},
    {'name': 'Burano', 'cat': 'Colored Board', 'cat_page': 'colored-boards.html', 'size': '70x100, 72x101', 'gsm': '250-320', 'desc': 'Smooth, vibrant coloured boards compatible with foil blocking and screen printing.'},
    {'name': 'Sumo', 'cat': 'Colored Board', 'cat_page': 'colored-boards.html', 'size': '71x101', 'gsm': '700-1050', 'desc': 'Solid tinted high-caliper boards with consistent internal colour distribution.'},
    {'name': 'Eco Cream', 'cat': 'White & Cream', 'cat_page': 'white-cream.html', 'size': '64x92, 67x98, 71x102', 'gsm': '300', 'desc': 'Smooth surface papers recommended for digital printing applications.'},
    {'name': 'Eco White', 'cat': 'White & Cream', 'cat_page': 'white-cream.html', 'size': 'Various Standard', 'gsm': '300, 350', 'desc': 'Bright white papers offering excellent printability for tags and cards.'},
    {'name': 'Biancoflash', 'cat': 'White & Cream', 'cat_page': 'white-cream.html', 'size': '70x100, 72x102', 'gsm': '120-400', 'desc': 'Calendered smooth paper available in master, natural and ivory shades.'},
    {'name': 'Kraft Board', 'cat': 'Kraft', 'cat_page': 'kraft.html', 'size': '70x100', 'gsm': '170-440', 'desc': '100% virgin pulp board designed for rigid packaging and stability.'},
    {'name': 'Kraft Paper', 'cat': 'Kraft', 'cat_page': 'kraft.html', 'size': '70x100', 'gsm': '100-300', 'desc': 'Specialist kraft papers suitable for printing and coating applications.'},
    {'name': 'Brilliant Black', 'cat': 'Black & Recycled', 'cat_page': 'black-recycled.html', 'size': '70x100', 'gsm': '90-350', 'desc': '100% recycled chlorine-free black tone papers with a rich finish.'},
    {'name': 'Raw Black', 'cat': 'Black & Recycled', 'cat_page': 'black-recycled.html', 'size': '72x102', 'gsm': '300-550', 'desc': 'Eco-friendly packaging compliant deep black boards from the Shiro Echo line.'},
    {'name': 'Textured Boards', 'cat': 'Textures', 'cat_page': 'textures.html', 'size': '72x102', 'gsm': '300', 'desc': 'Embossed boards optimized for high-end digital and offset printing texture.'},
    {'name': 'Shiro Echo', 'cat': 'Recycled Papers', 'cat_page': 'recycled-papers.html', 'size': '72x102', 'gsm': '90-300', 'desc': '100% post-consumer waste white and bright white papers for sustainable projects.'},
    {'name': 'Crush Corn', 'cat': 'Recycled Papers', 'cat_page': 'recycled-papers.html', 'size': '72x102', 'gsm': '250', 'desc': 'Unique sustainable papers made with 15% corn by-products.'},
    {'name': 'Matt Plain', 'cat': 'Covering', 'cat_page': 'covering-papers.html', 'size': '71x102, 76x102', 'gsm': '120', 'desc': 'Premium matt plain covering substrates offering vibrant colors and high tensile strength.'},
    {'name': 'Classy Covers', 'cat': 'Covering', 'cat_page': 'covering-papers.html', 'size': '72 x 102', 'gsm': '120', 'desc': 'Classy covers are the perfect embossed covering for books, binders and folders.'},
]

# Read index.html to steal the nav and mobile menu
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
except FileNotFoundError:
    print("Error: index.html not found.")
    exit(1)

# Extract Desktop Nav
nav_match = re.search(r'(<!-- FLOATING NAV \(DESKTOP\) -->.*?)</nav>', index_content, re.DOTALL)
desktop_nav = nav_match.group(0) if nav_match else ""

# Extract Mobile Header
mobile_header_match = re.search(r'(<!-- MOBILE HEADER.*?)</header>', index_content, re.DOTALL)
mobile_header = mobile_header_match.group(0) if mobile_header_match else ""

# Extract Mobile Overlay
# Ensure we capture the full structure including nested divs
mobile_overlay_match = re.search(r'(<!-- MOBILE NAVIGATION OVERLAY -->.*?<div class="mobile-nav-overlay">.*?</nav>\s*</div>)', index_content, re.DOTALL)
mobile_overlay = mobile_overlay_match.group(0) if mobile_overlay_match else ""

# Extract Footer
footer_match = re.search(r'(<footer.*?</footer>)', index_content, re.DOTALL)
footer = footer_match.group(0) if footer_match else ""


# Generate pages
for p in products:
    filename = p['name'].replace(' ', '-').lower() + '.html'
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{p['name']} | LEBA Speciality Papers</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.4/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.4/ScrollTrigger.min.js"></script>
</head>
<body>

    {desktop_nav}

    {mobile_header}

    {mobile_overlay}

    <div class="main-wrapper">
        <div class="product-hero">
            <div class="breadcrumb-custom">
                <span class="symbol">▼</span> Graphic Speciality » {p['cat']}
            </div>
            <h1 class="product-title">{p['name']}</h1>
            <p class="product-desc">{p['desc']}</p>
            
            <div style="position: absolute; right: 50px; top: 150px;" class="desktop-only">
                <a href="{p['cat_page']}" class="btn-more-products">
                    More Products in <strong>{p['cat']}</strong> +
                </a>
            </div>
    
            <div class="spec-container">
                <div class="spec-box">
                    <span class="spec-label">Size</span>
                    <span class="spec-value">{p['size']}</span>
                </div>
                <div class="spec-box" style="margin-left: 20px;">
                    <span class="spec-label">GSM</span>
                    <span class="spec-value">{p['gsm']}</span>
                </div>
            </div>
    
            <div class="apps-header">
                <div class="apps-grid-icon"><span></span><span></span><span></span><span></span></div>
                <div class="apps-title">Applications</div>
            </div>
            <div class="apps-divider"></div>
        </div>
        
        {footer}
    </div>

    <script src="main.js"></script>
</body>
</html>"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated {filename}")

print("All product pages generated successfully.")
