#!/usr/bin/env python3
"""
Jekyll to Ghost Migration Script
Converts Jekyll markdown posts to Ghost JSON import format.

Usage:
    python jekyll_to_ghost.py /path/to/jekyll/_posts output.json
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

def convert_to_ghost_json(posts_dir, output_file):
    """Convert Jekyll posts to Ghost JSON import format."""
    posts_path = Path(posts_dir).expanduser()
    
    if not posts_path.exists():
        print(f"Error: Directory not found: {posts_path}")
        return False
    
    posts_data = []
    tags_data = []
    posts_tags_data = []
    posts_authors_data = []
    
    tags_dict = {}
    tag_id_counter = 1
    post_id_counter = 1
    
    markdown_files = list(posts_path.glob('*.md'))
    if not markdown_files:
        print(f"Error: No markdown files found in {posts_path}")
        return False
    
    print(f"Found {len(markdown_files)} markdown files\n")
    
    for post_file in sorted(markdown_files):
        print(f"Processing: {post_file.name}")
        
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract front matter
            front_matter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
            
            if not front_matter_match:
                print(f"  Skipping: No front matter found")
                continue
            
            front_matter = front_matter_match.group(1)
            markdown_content = front_matter_match.group(2).strip()
            
            # Parse front matter fields
            title = re.search(r'title:\s*(.+)', front_matter)
            tags = re.search(r'tags:\s*\[(.*?)\]', front_matter)
            canonical = re.search(r'canonical_url:\s*(.+)', front_matter)
            status = re.search(r'status:\s*(.+)', front_matter)
            image = re.search(r'image:\s*(.+)', front_matter)
            
            # Extract date from filename
            date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})-(.+)\.md', post_file.name)
            if date_match:
                year, month, day, slug = date_match.groups()
                published_at = int(datetime(int(year), int(month), int(day)).timestamp() * 1000)
            else:
                published_at = int(datetime.now().timestamp() * 1000)
                slug = post_file.stem
            
            post_title = title.group(1).strip().strip('"\'') if title else post_file.stem
            post_status = status.group(1).strip() if status else "published"
            
            post_id = post_id_counter
            post_id_counter += 1
            
            # Fix image paths
            markdown_content = re.sub(r'\{\{\s*site\.baseurl\s*\}\}', '', markdown_content)
            markdown_content = markdown_content.replace('/assets/images/', '/content/images/')
            markdown_content = re.sub(r'http://localhost:\d+', '', markdown_content)
            
            # Convert to mobiledoc
            mobiledoc = {
                "version": "0.3.1",
                "atoms": [],
                "cards": [["markdown", {"markdown": markdown_content}]],
                "markups": [],
                "sections": [[10, 0]]
            }
            
            # Build post
            post = {
                "id": post_id,
                "uuid": f"ghost-{post_id}-{slug[:20]}",
                "title": post_title,
                "slug": slug,
                "mobiledoc": json.dumps(mobiledoc),
                "html": None,
                "comment_id": post_id,
                "featured": 0,
                "type": "post",
                "status": post_status,
                "locale": None,
                "visibility": "public",
                "email_recipient_filter": "all",
                "author_id": 1,
                "created_at": published_at,
                "created_by": 1,
                "updated_at": published_at,
                "updated_by": 1,
                "published_at": published_at if post_status == "published" else None,
                "published_by": 1 if post_status == "published" else None,
                "custom_excerpt": None,
                "codeinjection_head": None,
                "codeinjection_foot": None,
                "custom_template": None,
                "canonical_url": canonical.group(1).strip() if canonical else None
            }
            
            # Add feature image
            if image:
                image_path = image.group(1).strip().strip('"\'')
                if image_path.startswith('/assets/images/'):
                    image_path = image_path.replace('/assets/images/', '/content/images/')
                elif image_path.startswith('assets/images/'):
                    image_path = '/content/images/' + image_path.replace('assets/images/', '')
                post["feature_image"] = image_path
                print(f"  Feature image: {image_path}")
            else:
                post["feature_image"] = None
            
            # Handle tags
            post_tag_ids = []
            if tags:
                tag_list = [t.strip().strip('"\'') for t in tags.group(1).split(',')]
                
                for tag_name in tag_list:
                    if tag_name:
                        if tag_name not in tags_dict:
                            tag_id = tag_id_counter
                            tag_id_counter += 1
                            tags_dict[tag_name] = tag_id
                            tags_data.append({
                                "id": tag_id,
                                "name": tag_name,
                                "slug": tag_name.lower().replace(' ', '-').replace(',', '').replace('&', 'and')
                            })
                        
                        post_tag_ids.append(tags_dict[tag_name])
            
            # Create relationships
            for idx, tag_id in enumerate(post_tag_ids):
                posts_tags_data.append({
                    "id": f"{post_id}-{tag_id}",
                    "post_id": post_id,
                    "tag_id": tag_id,
                    "sort_order": idx
                })
            
            posts_authors_data.append({
                "id": post_id,
                "post_id": post_id,
                "author_id": 1,
                "sort_order": 0
            })
            
            posts_data.append(post)
            print(f"  Added: {post_title}")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    # Create Ghost JSON
    ghost_json = {
        "db": [{
            "meta": {
                "exported_on": int(datetime.now().timestamp() * 1000),
                "version": "5.130.5"
            },
            "data": {
                "posts": posts_data,
                "tags": tags_data,
                "posts_tags": posts_tags_data,
                "posts_authors": posts_authors_data
            }
        }]
    }
    
    # Write output
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(ghost_json, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"\nError writing file: {e}")
        return False
    
    print(f"\nSuccess! Created: {output_file}")
    print(f"Posts: {len(posts_data)} | Tags: {len(tags_data)}")
    print(f"\nNext steps:")
    print(f"Import {output_file} in Ghost Admin > Settings > Labs")
    
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python jekyll_to_ghost.py <posts_dir> [output_file]")
        print("Example: python jekyll_to_ghost.py ~/blog/_posts ghost-import.json")
        sys.exit(1)
    
    posts_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'ghost-import.json'
    
    success = convert_to_ghost_json(posts_dir, output_file)
    sys.exit(0 if success else 1)