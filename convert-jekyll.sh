#!/bin/bash
mkdir -p ghost-import

# Use the full path to _posts directory
for file in ./_posts/*.md; do
  echo "Processing file: $file"
  filename=$(basename "$file")
  
  # Create Ghost-compatible front matter
  sed -E '
    # Convert layout: post to status: published
    s/layout: post/status: published/g
    # Keep title as is
    # Keep tags as is
    # Remove site.baseurl from image references
    s/\{\{ site\.baseurl \}\}//g
    s|/assets/images/|/content/images/|g
  ' "$file" > ghost-import/"$filename"
done

echo "Conversion complete. Files in ghost-import/"