import glob
import re

files = glob.glob('frontend/templates/*.html')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove the nav-admin button
    new_content = re.sub(r'<a href="/pages/admin\.html".*?id="nav-admin".*?>Admin</a>\s*', '', content)
    
    # Also remove the one in contact.html if any
    new_content = re.sub(r'<a href="/pages/admin\.html".*?>→ Admin Panel</a>\s*', '', new_content)
    
    if content != new_content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Removed from {f}")
