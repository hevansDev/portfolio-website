import os
import json
import re
from pathlib import Path
from datetime import datetime

def convert_to_ghost_json_with_images(posts_dir, output_file):
    posts_path = Path(posts_dir)
    
    posts_data = []
    tags_data = []
    posts_tags_data = []
    posts_authors_data = []
    
    tags_dict = {}
    tag_id_counter = 1
    post_id_counter = 1
    
    for post_file in sorted(posts_path.glob('*.md')):
        print(f"Processing: {post_file.name}")
        
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract front matter
            front_matter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
            
            if not front_matter_match:
                print(f"Skipping {post_file.name}: No front matter found")
                continue
            
            front_matter = front_matter_match.group(1)
            markdown_content = front_matter_match.group(2).strip()
            
            # Parse front matter
            title = re.search(r'title:\s*(.+)', front_matter)
            tags = re.search(r'tags:\s*\[(.*?)\]', front_matter)
            canonical = re.search(r'canonical_url:\s*(.+)', front_matter)
            status = re.search(r'status:\s*(.+)', front_matter)
            image = re.search(r'image:\s*(.+)', front_matter)  # NEW: Extract image
            
            # Extract date from filename
            date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})-(.+)\.md', post_file.name)
            if date_match:
                year, month, day, slug = date_match.groups()
                published_at = int(datetime(int(year), int(month), int(day)).timestamp() * 1000)
                slug = slug
            else:
                published_at = int(datetime.now().timestamp() * 1000)
                slug = post_file.stem
            
            post_title = title.group(1).strip().strip('"') if title else post_file.stem
            post_status = status.group(1).strip() if status else "published"
            
            post_id = post_id_counter
            post_id_counter += 1
            
            # Convert markdown to mobiledoc
            mobiledoc = {
                "version": "0.3.1",
                "atoms": [],
                "cards": [["markdown", {"markdown": markdown_content}]],
                "markups": [],
                "sections": [[10, 0]]
            }
            
            # Build post object
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
            
            # NEW: Add feature image if it exists
            if image:
                image_path = image.group(1).strip()
                # Convert /assets/images/filename.png to /content/images/filename.png
                if image_path.startswith('/assets/images/'):
                    image_path = image_path.replace('/assets/images/', '/content/images/')
                post["feature_image"] = image_path
                print(f"  Feature image: {image_path}")
            else:
                post["feature_image"] = None
            
            # Handle tags
            post_tag_ids = []
            if tags:
                tag_list = [t.strip().strip('"') for t in tags.group(1).split(',')]
                
                for tag_name in tag_list:
                    if tag_name:
                        if tag_name not in tags_dict:
                            tag_id = tag_id_counter
                            tag_id_counter += 1
                            tags_dict[tag_name] = tag_id
                            tags_data.append({
                                "id": tag_id,
                                "name": tag_name,
                                "slug": tag_name.lower().replace(' ', '-').replace(',', '')
                            })
                        
                        post_tag_ids.append(tags_dict[tag_name])
            
            # Create post-tag relationships
            for idx, tag_id in enumerate(post_tag_ids):
                posts_tags_data.append({
                    "id": f"{post_id}-{tag_id}",
                    "post_id": post_id,
                    "tag_id": tag_id,
                    "sort_order": idx
                })
            
            # Create post-author relationship
            posts_authors_data.append({
                "id": post_id,
                "post_id": post_id,
                "author_id": 1,
                "sort_order": 0
            })
            
            posts_data.append(post)
            print(f"✓ Added: {post_title}")
            
        except Exception as e:
            print(f"✗ Error processing {post_file.name}: {e}")
            import traceback
            traceback.print_exc()
    
    # Create Ghost JSON structure
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
    
    # Write JSON file
    output_path = Path(output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(ghost_json, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Created Ghost import file: {output_file}")
    print(f"Total posts: {len(posts_data)}")
    print(f"Total tags: {len(tags_data)}")
    print(f"Total post-tag relationships: {len(posts_tags_data)}")
    print(f"Total post-author relationships: {len(posts_authors_data)}")

# Usage
convert_to_ghost_json_with_images('./', 'ghost-import-with-featured-images.json')