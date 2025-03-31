---
title: Adventures in POSSE
tags: [Article, POSSE, IndieWeb]
layout: post
image: /assets/images/anne-fehres_luke-conroy_ai4media_hidden-labour-of-internet-browsing_2560x1440.jpg
---

<meta property="og:image" content="{{ site.url }}/assets/images/anne-fehres_luke-conroy_ai4media_hidden-labour-of-internet-browsing_2560x1440.jpg">

![A collage picturing a chaotic intersection filled with reCAPTCHA items like crosswalks, fire hydrants and traffic lights, representing the unseen labor in data labelling.]({{ site.baseurl }}/assets/images/anne-fehres_luke-conroy_ai4media_hidden-labour-of-internet-browsing_2560x1440.jpg)
<span><a href="https://www.annefehres.com/">Anne Fehres and Luke Conroy</a> & <a href="https://www.luke-conroy.com/">AI4Media</a> / <a href="https://www.betterimagesofai.org">Better Images of AI</a> / Hidden Labour of Internet Browsing / <a href="https://creativecommons.org/licenses/by/4.0/">Licensed by CC-BY 4.0</a></span>

## Post Own Site Syndicate Everywhere

[POSSE](https://indieweb.org/POSSE) (Post [on your] Own Site Syndicate Everywhere) is a simple concept: when you create digital content like articles, guides, or videos simply upload it to your own website before posting links back to that content on third party sites like Medium or YouTube. One key advantage of this approach is it provides a degree of indepdence from third party platforms as all your content is preserved on your site so the loss of a social media account doesn't mean losing years of work.

I first learned about POSSE in [the excellent article of the same title by Molly White](https://www.citationneeded.news/posse/) and have since adopted the approach for my own work.

An issue often sited with POSSE is that posting content across multiple channels can be labour intensive either as a result of the work required in manually posting via several third party platforms or maintaining the tooling required to automate the process. There are some ongoing efforts to help simplify the process of cross posting across multiple channels including Ryan Barrett's [Bridgy Fed](https://fed.brid.gy/) project which serves as a bridge between decentralized social networks.

I wanted to build POSSE into my existing [CICD](https://github.com/resources/articles/devops/ci-cd) for my site which I have configured as [GitHub Actions](https://github.com/features/actions) - I decided to (perhaps foolishly) write a few quick scripts to post links to new articles on my Website to my various social media accounts which proved tricker than I expected! In this article I'll talk you through my attempt at automating the common POSSE task of reposting links with a hope that elements of it may be useful to your own projects. All my code is available on my [GitHub](https://github.com/hevansDev/portfolio-website).

## Posting on your own site...

I'm using [Jekyll](https://jekyllrb.com/) a Ruby based static website generator along with the awesome [Contrast theme by Niklas Buschmann](https://niklasbuschmann.github.io/contrast/) for my personal site. I use GitHub Actions workflows to to build the static HTML from my Jekyll project and then copy it across to an Nginx server running on a Raspberry Pi in my Homelab.

![A screenshot of a successfully completed github action for building and deploying a jekyll site]({{ site.baseurl }}/assets/images/gha_screenshot.png)
*A screenshot of a successfully completed github action for building and deploying a jekyll site*

I like being able to write my posts in both HTML and Markdown because of the flexibility it provides so this approach works well for me - it also makes it easy to edit content already published to my site. I can also test what articles will look like by running Jekyll locally which is really helpful for catching mistakes prior to publishing.

## ...and syndicate everywhere!

Once I've written a new article I want to link to it from all the other places I have a presence on the internet like Bluesky, LinkedIn, and Mastodon. Frustratingly at time of writing LinkedIn doesn't appear to provide any methods for posting to your own LinkedIn account with their API - instead only allowing you to [post to a company page](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?view=li-lms-2024-10&tabs=http) so for now I'm limited to (still two great options!) Bluesky and Mastodon.

### Getting new posts from a PR

Before I can post any links to articles I need to get new articles from PRs merged to my repo. All the articles on my site are stored in a directory called `_posts` so it's easy enough to get a list of articles by running the handy [`changed-files`](https://github.com/tj-actions/changed-files) action against that directory.

```
- name: Get changed files
    id: changed-files
    uses: tj-actions/changed-files@v45.0.4
    with:
    files: |
        _posts/**
```

Once I have a list of all the new articles I can easily iterate over them with a Bash loop. At the moment though this list is of file paths rather than links to the actual articles but this is easy enough to fix by extracting the name of the articles from the file path and appending it to the site url.

```
- name: Post all new posts
    if: steps.changed-files.outputs.any_changed == 'true'
    env:
    ALL_NEW_POSTS: ${{ steps.changed-files.outputs.added_files }}
    run: |
    
    for file in ${ALL_NEW_POSTS}; do
        echo $file
        # Get new post URLs from diff
        blog_url="https://hughevans.dev/${file:18:-3}"
```

Now that I can get a url for each new article it's relatively simple to just POST that url in the text field of a post to the social media platform of my choice.

### Mastodon

Posting a link to Mastodon and getting a nice embedded card is really easy as Mastodon pulls out all the [OpenGraph](https://ogp.me/) information and renders it automatically for you into a nice [preview card](https://box464.com/posts/mastodon-preview-cards/).

All you need to POST via the Mastodon API is your user token which can be found under Preferences > Development ([see the Mastodon docs](https://docs.joinmastodon.org/client/intro/) for more information).

With my list of new articles I can easily use the below POST request via curl to create a post on Mastodon with a nice preview card for my articles.

```
# Post to Mastodon
curl -X POST -d "{\"status\":\"$blog_url\", \
\"media_ids\":null,\"poll\":null}" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${{secrets.MASTODON_USER_TOKEN}}" \
"https://hachyderm.io/api/v1/statuses"
```

Ta-dah!

![A post on mastodon with a link to a blog about me speaking at the Barcelona Aerospike Meetup]({{ site.baseurl }}/assets/images/mastodon-post.png)
*A post on mastodon with a link to a blog about me speaking at the Barcelona Aerospike Meetup*

### Bluesky

I found posting an embed card to Bluesky much trickier than posting via the Mastodon API (as anyone unfortunate enough to be following me on Bluesky whilst I was writing this article probably noticed!)

I found [these examples](https://gist.github.com/pojntfx/72403066a96593c1ba8fd5df2b531f2d) shared by [Felicitas Pojtinger](https://gist.github.com/pojntfx) really helpful but my main stumbling block was that I needed to manually include the OpenGraph information as fields in the body of my post requests as [Bluesky won't detect this automatically yet](https://github.com/bluesky-social/social-app/issues/1672).

Before posting via the API you need to create a new app password under Settings > Privacy and Security > App Passwords. I learned that posting to Bluesky isn't as simple as just making a POST request with my app password, as a result of running on the decentralized [AT Protocol](https://atproto.com/), posting via the API required that I find the [Decentralized Identifier (or DID)](https://atproto.com/specs/did) for my handle and with that get a session API key - I did both of these with the pair of curl commands in the Bash snippet below.

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
```

Once I had an API key posting text to Bluesky was simple, however: I wanted to create a preview card with an embedded image and an article title. I couldn't find any neat way to do this directly in the Bluesky API - as a work around I used the snippet below to pull the Open Graph data from the blog post automatically so I can pass it in the Bluesky POST body.

```
# Get page og image
og_img_url=$(curl -L $blog_url | grep 'og.image' | grep -oE "(http|https)://[a-zA-Z0-9./?=_%:-]*")
curl -O $og_img_url

# Get page title
page_title=$(curl $blog_url -so - | grep -o "<title>[^<]*" | tail -c+8)
```

So with all that done I should be ready to POST the link right? No such luck. The embed image first needs to be uploaded as a blob and the blob link and size recorded for use in the POST.

```
# Upload embed image blob
blob=$(curl -X POST \
    -H "Authorization: Bearer ${API_KEY}" \
    -H 'Content-Type: image/jpeg' \
    --data-binary @$(ls *.jpg) \
    "https://bsky.social/xrpc/com.atproto.repo.uploadBlob")


blob_size=$(echo $blob | jq  '.blob.size')

blob_link=$(echo $blob | jq  '.blob.ref."$link"')
```

Finally, I can post the link - I can POST an empty text post to Bluesky which includes an embed with a link to my new post, the post title, link to the upload image blob, and the size of that blob.

```
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

That POST gets us this final result.

![A post on Bluesky with a link to a blog about me speaking at the Barcelona Aerospike Meetup]({{ site.baseurl }}/assets/images/bluesky-post.png)
*A post on Bluesky with a link to a blog about me speaking at the Barcelona Aerospike Meetup*

## Final thoughts

I had a lot of fun playing around with automating posting for POSSE and learning a little bit about the nuances of the Bluesky API and AT Proto. In future I'd like to expand on this project with integrations for other channels like Medium - I think I'll most likely explore using existing tooling rather than building my own because of how unwieldy my implementation has ended up being. 