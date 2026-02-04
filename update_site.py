
import os
import re

css_to_append = """
/* --- 3-LEVEL NAVIGATION STYLES --- */

/* Less invasive parent indicator */
.nav-item .dropdown-parent::after {
  content: "";
  display: inline-block;
  width: 0;
  height: 0;
  margin-left: 6px;
  vertical-align: middle;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid currentColor;
  opacity: 0.6;
}

/* PRODUCT PAGE STYLES (LEVEL 3) */
.product-hero {
  text-align: center;
  padding: 80px 20px;
  background: var(--bg-surface);
  margin-top: 100px;
}

.breadcrumb-custom {
  font-family: var(--font-main);
  font-size: 0.85rem;
  color: var(--color-secondary);
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.breadcrumb-custom .symbol {
  font-size: 0.6rem;
  opacity: 0.7;
}

.product-title {
  font-family: var(--font-main);
  font-size: 3.5rem;
  font-weight: 300;
  letter-spacing: -0.03em;
  margin-bottom: 20px;
  color: var(--color-primary);
}

.product-desc {
  max-width: 700px;
  margin: 0 auto 40px;
  font-family: var(--font-main);
  font-size: 1.05rem;
  color: var(--color-secondary);
  line-height: 1.6;
  font-weight: 300;
}

.spec-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  margin: 50px 0;
}

.spec-box {
  width: 260px;
  height: 100px;
  background: linear-gradient(135deg, #3b597b 0%, #7d2e46 100%);
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 10px 30px -10px rgba(60, 40, 80, 0.3); 
  border: none;
  border-radius: 4px; /* Slight round */
}

.spec-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 6px;
  opacity: 0.9;
}

.spec-value {
  font-family: var(--font-main);
  font-size: 1.3rem;
  font-weight: 500;
  letter-spacing: -0.01em;
}

.apps-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 40px;
}

.apps-grid-icon {
  display: grid;
  grid-template-columns: repeat(2, 6px);
  gap: 3px;
}

.apps-grid-icon span {
  width: 6px;
  height: 6px;
  background: var(--color-primary);
  opacity: 0.8;
}

.apps-title {
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--color-primary);
}

.apps-divider {
  width: 1px;
  height: 80px;
  background: linear-gradient(to bottom, #ddd, transparent);
  margin: 0 auto;
}

.btn-more-products {
  background: var(--color-primary);
  color: white;
  padding: 12px 28px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
  border-radius: 4px;
}

/* --- MOBILE NESTED ACCORDION THEME --- */

.mobile-submenu {
    background: #f9f9f9;
}

.mobile-dropdown-inner {
    border-bottom: 1px solid rgba(0,0,0,0.03);
}

.submenu-parent-link {
    background: none;
    border: none;
    font-size: 1rem;
    font-weight: 500;
    color: var(--color-secondary);
    padding: 16px 24px;
    padding-left: 40px; 
    width: 100%;
    text-align: left;
    cursor: pointer;
    font-family: var(--font-main);
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background 0.2s;
}

.submenu-parent-link:hover {
    background: rgba(0,0,0,0.02);
}

.mobile-submenu-l3 {
    display: none;
    flex-direction: column;
    background: #f0f0f0; 
    padding-top: 5px;
    padding-bottom: 15px;
}

.is-open .mobile-submenu-l3 {
    display: flex;
    animation: slideDown 0.3s ease-out;
}

.submenu-link-l3 {
    font-size: 0.95rem;
    color: #666;
    padding: 12px 24px;
    padding-left: 60px;
    transition: color 0.2s;
    display: block;
}

.submenu-link-l3:hover {
    color: var(--color-accent);
    background: rgba(255,255,255,0.5);
}

.submenu-parent-link::after {
    content: "+"; 
    font-weight: 300; 
    font-size: 1.4rem;
    color: var(--color-primary);
    opacity: 0.4;
}

.mobile-dropdown-inner.is-open .submenu-parent-link::after {
    content: "-";
}
"""

def update_css():
    try:
        with open('styles.css', 'r', encoding='utf-8') as f:
            content = f.read()
            if "/* --- MOBILE NESTED ACCORDION THEME --- */" in content:
                print("CSS styles already present.")
                return

        with open('styles.css', 'a', encoding='utf-8') as f:
            f.write(css_to_append)
        print("Styles appended to styles.css")
    except Exception as e:
        print(f"Error updating CSS: {e}")

def update_html_files():
    # Files to update
    files = [
        'company.html', 'applications.html', 'capabilities.html', 
        'contact.html', 'products.html', 
        'covering-papers.html', 'colored-boards.html', 'white-cream.html', 'kraft.html', 
        'black-recycled.html', 'textures.html', 'recycled-papers.html', 
        'art-papers.html', 'premium-print.html', 'textured-finish.html', 'coated-specialty.html'
    ]

    # Source content from index.html
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            index_content = f.read()
    except FileNotFoundError:
        print("index.html not found.")
        return

    # Extract Nav and Overlay
    nav_match = re.search(r'(<!-- FLOATING NAV \(DESKTOP\) -->.*?</nav>)', index_content, re.DOTALL)
    
    # Improved regex: Look for the div class "mobile-nav-overlay" until the end of its nav/div structure
    # Since capturing nested divs with regex is hard, we rely on the specific closing pattern </nav>\s*</div> which seems consistent
    overlay_match = re.search(r'(<div class="mobile-nav-overlay">.*?</nav>\s*</div>)', index_content, re.DOTALL)
    
    if not nav_match or not overlay_match:
        print("Could not find nav or overlay in index.html")
        return

    new_nav = nav_match.group(1)
    new_overlay = overlay_match.group(1)

    for file_name in files:
        if not os.path.exists(file_name):
            print(f"Skipping {file_name} (not found)")
            continue
            
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace Desktop Nav (Assuming it has the comment)
            content = re.sub(r'(<!-- FLOATING NAV \(DESKTOP\) -->.*?</nav>)', lambda m: new_nav, content, flags=re.DOTALL)
            
            # Replace Mobile Overlay - Flexible match
            # Try matching with comment first (old files)
            content = re.sub(r'(<!-- MOBILE NAVIGATION OVERLAY -->.*?<div class="mobile-nav-overlay">.*?</nav>\s*</div>)', lambda m: new_overlay, content, flags=re.DOTALL)
            
            # Try matching without comment (newly generated files) if previous didn't change anything?
            # Actually, just matching the div content is safer if we know the boundary
            content = re.sub(r'(<div class="mobile-nav-overlay">.*?</nav>\s*</div>)', lambda m: new_overlay, content, flags=re.DOTALL)
            
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {file_name}")
            
        except Exception as e:
            print(f"Error updating {file_name}: {e}")

if __name__ == "__main__":
    update_css()
    update_html_files()
