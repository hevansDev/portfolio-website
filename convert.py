import os
import re
from pathlib import Path

def convert_jekyll_to_ghost(jekyll_dir, output_dir):
    input_path = Path(jekyll_dir)
    
    # Check if _posts exists, otherwise use the directory itself
    if (input_path / '_posts').exists():
        posts_dir = input_path / '_posts'
    else:
        posts_dir = input_path
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    converted_count = 0
    
    for post_file in posts_dir.glob('*.md'):
        print(f"Processing: {post_file.name}")
        
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix canonicalurl to canonical_url
            content = re.sub(r'canonicalurl:', 'canonical_url:', content)
            
            # Write to output
            output_file = output_path / post_file.name
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Converted: {post_file.name}")
            converted_count += 1
            
        except Exception as e:
            print(f"✗ Error processing {post_file.name}: {e}")
    
    print(f"\nTotal posts converted: {converted_count}")

# Usage - safer approach with separate output
convert_jekyll_to_ghost('./ghost-import', './ghost-output')