---
title: Practical POSSE made easy
tags: [HowTo, POSSE, API, OSS, Article]
layout: post
---

<meta property="og:image" content="{{ site.url }}/assets/images/anne-fehres_luke-conroy_ai4media_hidden-labour-of-internet-browsing_2560x1440.jpg">

![A collage picturing a chaotic intersection filled with reCAPTCHA items like crosswalks, fire hydrants and traffic lights, representing the unseen labor in data labelling.]({{ site.baseurl }}/assets/images/anne-fehres_luke-conroy_ai4media_hidden-labour-of-internet-browsing_2560x1440.jpg)
<span><a href="https://www.annefehres.com/">Anne Fehres and Luke Conroy</a> & <a href="https://www.luke-conroy.com/">AI4Media</a> / <a href="https://www.betterimagesofai.org">Better Images of AI</a> / Hidden Labour of Internet Browsing / <a href="https://creativecommons.org/licenses/by/4.0/">Licenced by CC-BY 4.0</a></span>

## Post Own Site Syndicate Everywhere

[POSSE](https://indieweb.org/POSSE) (Post [on your] Own Site Syndicate Everywhere) is a simple concept: when you create digital content like articles, guides, or videos upload it to your own website before posting links back to that content on third party sites like Medium or YouTube. One key advantage of this approach is it provides a degree of indepdence from third party platforms as all your content is preserved on your site.

I first learned about POSSE in [the excellent article of the same title by Molly White](https://www.citationneeded.news/posse/) and have since adopted the approach for my own work.

An issue often sited with POSSE is that posting content across multiple channels can be labour intensive either as a result of the work required in manually posting via several third party platforms or maintaining the tooling required to automate the process. There are some ongoing efforts to help simplify the process of cross posting across multiple channels including Ryan Barrett's [Bridgy Fed](https://fed.brid.gy/) project which serves as a bridge between decentralized social networks.

My background is in DevOps so I wanted to build POSSE into my existing [CICD](https://github.com/resources/articles/devops/ci-cd) for my site which I have configured as [GitHub Actions](https://github.com/features/actions) - I decided to (perhaps foolishly) write a few quick scripts to post links to new articles on my Website to my various social media accounts which proved tricker than I expected! In this article I'll outline how I'm doing POSSE with a hope that elements of it may be useful to your own projects.

## Posting on your own site...

I'm using [Jekyll](https://jekyllrb.com/) a Ruby based static website generator with the awesome [Contrast theme by Niklas Buschmann](https://niklasbuschmann.github.io/contrast/) for my personal site. I use a custom GitHub Actions workflow to run Jekyll to build my site and copy it across to an Nginx server 

## ...and syndicate everywhere!

### Mastodon

https://box464.com/posts/mastodon-preview-cards/

```
# Post to Mastodon
curl -X POST -d "{\"status\":\"$blog_url\", \
\"media_ids\":null,\"poll\":null}" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${{secrets.MASTODON_USER_TOKEN}}" \
"https://hachyderm.io/api/v1/statuses"
```

### Bluesky

```
# Post to Bluesky
export APP_PASSWORD='${{secrets.BLUESKY_APP_PASSWORD}}'

HANDLE='hevansdev.bsky.social'
DID_URL="https://bsky.social/xrpc/com.atproto.identity.resolveHandle"
export DID=$(curl -G \
    --data-urlencode "handle=$HANDLE" \
    "$DID_URL" | jq -r .did)

# Get API key with the app password
API_KEY_URL='https://bsky.social/xrpc/com.atproto.server.createSession'
POST_DATA="{ \"identifier\": \"${DID}\", \"password\": \"${APP_PASSWORD}\" }"
export API_KEY=$(curl -X POST \
    -H 'Content-Type: application/json' \
    -d "$POST_DATA" \
    "$API_KEY_URL" | jq -r .accessJwt)

# Get page og image
og_img_url=$(curl -L $blog_url | grep 'og.image' | grep -oE "(http|https)://[a-zA-Z0-9./?=_%:-]*")
curl -O $og_img_url

# Get page title
page_title=$(curl $blog_url -so - | grep -o "<title>[^<]*" | tail -c+8)

# Upload embed image blob
blob=$(curl -X POST \
    -H "Authorization: Bearer ${API_KEY}" \
    -H 'Content-Type: image/jpeg' \
    --data-binary @$(ls *.jpg) \
    "https://bsky.social/xrpc/com.atproto.repo.uploadBlob")


blob_size=$(echo $blob | jq  '.blob.size')

blob_link=$(echo $blob | jq  '.blob.ref."$link"')

# Site embed
POST_FEED_URL='https://bsky.social/xrpc/com.atproto.repo.createRecord'
POST_RECORD="{ \"collection\": \"app.bsky.feed.post\",
\"repo\": \"${DID}\",
\"record\": {
\"text\": \"\",
\"\$type\": \"app.bsky.feed.post\",
\"createdAt\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",
\"embed\": {
    \"\$type\": \"app.bsky.embed.external\",
        \"external\": {
            \"uri\": \"$blog_url\",
            \"title\": \"$page_title\",
            \"description\": \"\",
            \"thumb\": {
                \"\$type\": \"blob\",
                \"ref\": {
                    \"\$link\": $blob_link
                },
                \"mimeType\": \"image/jpeg\",
                \"size\": $blob_size } 
            }
        }
    } 
}"
curl -X POST \
    -H "Authorization: Bearer ${API_KEY}" \
    -H 'Content-Type: application/json' \
    -d "$POST_RECORD" \
    "$POST_FEED_URL" | jq -r
```