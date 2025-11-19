import json
from datetime import datetime

# Create a minimal test import
test_import = {
    "db": [{
        "meta": {
            "exported_on": int(datetime.now().timestamp() * 1000),
            "version": "5.0.0"
        },
        "data": {
            "posts": [{
                "id": 100,
                "uuid": "test-post-12345",
                "title": "Test Import Post",
                "slug": "test-import-post",
                "mobiledoc": '{"version":"0.3.1","atoms":[],"cards":[["markdown",{"markdown":"This is a test post to verify imports are working."}]],"markups":[],"sections":[[10,0]]}',
                "status": "published",
                "created_at": int(datetime.now().timestamp() * 1000),
                "published_at": int(datetime.now().timestamp() * 1000),
                "updated_at": int(datetime.now().timestamp() * 1000)
            }],
            "tags": [],
            "posts_tags": [],
            "posts_authors": [{
                "id": 100,
                "post_id": 100,
                "author_id": 1,
                "sort_order": 0
            }]
        }
    }]
}

with open('test-import.json', 'w') as f:
    json.dump(test_import, f, indent=2)

print("Created test-import.json - upload this to Ghost")