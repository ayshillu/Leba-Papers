
import os
import re

IMAGES_BASE = 'productimages'

CSS_APPEND = """
/* PRODUCT SAMPLE GALLERY */
.sample-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 1px;
    background: #e5e5e5;
    border: 1px solid #e5e5e5;
    margin-top: 40px;
    margin-bottom: 60px;
}

.sample-item {
    background: white;
    padding: 24px;
    text-align: center;
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    height: 100%;
    text-decoration: none;
    color: inherit;
}

.sample-item:hover {
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    position: relative;
    z-index: 10;
    transform: translateY(-2px);
    color: var(--color-accent);
}

.sample-item img {
    max-width: 100%;
    height: auto;
    object-fit: contain;
    margin-bottom: 20px;
    max-height: 200px;
}

.sample-title {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    color: inherit;
    letter-spacing: 0.05em;
    margin-top: auto;
}

.tit-cont {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.lineCls {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;
    opacity: 0.3;
}

.lineCls .line {
    width: 20px;
    height: 1px;
    background: currentColor;
}

.lineCls .circle {
    width: 3px;
    height: 3px;
    background: currentColor;
    border-radius: 50%;
    margin-left: 4px;
}
"""

MAPPING = {
    'matt-plain': 'covering/matt-plain',
    'buckram': 'covering/buckram',
    'classy-covers': 'covering/classy-covers',
    'glossy': 'covering/Glossy',
    'burano': 'colored-board/burano',
    'sumo': 'colored-board/Sumo',
    'eco-cream': 'white-cream/eco-cream',
    'eco-white': 'EcoWhite',
    'biancoflash': 'Biancoflash',
    'brilliant-black': 'BrilliantBlack',
    'raw-black': 'ShiroEchoRawBlack',
    'shiro-echo-raw-black': 'ShiroEchoRawBlack',
    'shiro-echo': 'ShiroEcho',
    'crush-corn': 'CrushCorn',
    'textured-boards': 'Textures',
    'kraft-board': 'kraft', 
    'kraft-paper': 'kraft',
    'majetstic': 'Majestic',
    'tube': 'Tube',
    'vintage': 'Vintage',
    'influience': 'Influience',
    'hammer': 'Hammer',
    'prisma': 'Prisma',
    'laid': 'Laid',
    'twill': 'Twill',
    'favini-20': 'Favini-20',
    'favini-35': 'Favini-35',
    'favini-60': 'Favini-60',
    'art-papers': 'Favini-20', # Default to something for art
    'premium-print': 'Vintage', # Default
}

def update_css():
    if os.path.exists('styles.css'):
        with open('styles.css', 'r', encoding='utf-8') as f:
            content = f.read()
        if "/* PRODUCT SAMPLE GALLERY */" not in content:
            with open('styles.css', 'a', encoding='utf-8') as f:
                f.write(CSS_APPEND)
            print("CSS appended.")
        else:
            print("CSS already present.")

def generate_gallery_html(image_folder_path, web_path_base):
    html = []
    html.append('<section class="panel reveal-panel" style="padding-top: 0;">')
    html.append('    <div class="container">')
    html.append('        <div class="sample-grid">')

    # Look for "thumb" folder
    thumb_dir = os.path.join(image_folder_path, 'thumb')
    big_dir = os.path.join(image_folder_path, 'big')
    
    images = []
    
    if os.path.exists(thumb_dir):
        for f in os.listdir(thumb_dir):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                title = os.path.splitext(f)[0].replace('-', ' ').title()
                thumb_path = f"{web_path_base}/thumb/{f}"
                big_path = f"{web_path_base}/big/{f}" # Assume big exists
                images.append((title, thumb_path, big_path))
    else:
        # Flat folder
        for f in os.listdir(image_folder_path):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                if 'thumb' in f.lower() or 'big' in f.lower(): continue # skip self if mixed?
                title = os.path.splitext(f)[0].replace('-', ' ').title()
                thumb_path = f"{web_path_base}/{f}"
                big_path = f"{web_path_base}/{f}"
                images.append((title, thumb_path, big_path))
    
    if not images:
        return ""

    for title, thumb, big in images:
        html.append(f'''
            <a href="{big}" class="sample-item" title="{title}">
                <img src="{thumb}" alt="{title}" loading="lazy">
                <div class="tit-cont">
                    <div class="lineCls">
                        <div class="line"></div>
                        <div class="circle"></div>
                    </div>
                    <div class="sample-title">{title}</div>
                </div>
            </a>
        ''')

    html.append('        </div>')
    html.append('    </div>')
    html.append('</section>')
    
    return "\n".join(html)

def process_files():
    for filename in os.listdir('.'):
        if not filename.endswith('.html'):
            continue
            
        base_name = os.path.splitext(filename)[0]
        
        if base_name in MAPPING:
            rel_folder = MAPPING[base_name]
            image_fs_path = os.path.join(IMAGES_BASE, rel_folder)
            
            if not os.path.exists(image_fs_path):
                print(f"Skipping {filename}: Image folder {rel_folder} not found")
                continue
                
            gallery_html = generate_gallery_html(image_fs_path, f"productimages/{rel_folder}")
            
            if not gallery_html:
                continue

            print(f"Injecting gallery into {filename}")
            
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Injection logic
            # Avoid duplicate injection
            if 'sample-grid' in content:
                print(f"Already injected in {filename}")
                continue

            # Inject before footer
            if '<footer' in content:
                new_content = content.replace('<footer', f'{gallery_html}\n<footer', 1)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Success: {filename}")
            else:
                print(f"No footer found in {filename}")

if __name__ == "__main__":
    update_css()
    process_files()
