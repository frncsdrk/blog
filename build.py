#!/usr/bin/env python3

import os

# constants
_TEMPLATES_DIR = "_templates"
_POSTS_DIR = "_posts"
POSTS_DIR = "posts"
POST_META_PLACEHOLDER = "{{ post_meta }}"
POST_TITLE_PLACEHOLDER = "{{ post_title }}"
POST_CONTENT_PLACEHOLDER = "{{ post_content }}"
POSTS_LIST_PLACEHOLDER = "{{ posts_list }}"
POST_SUMMARY_META_PLACEHOLDER = "{{ post_meta }}"
POST_SUMMARY_HREF_PLACEHOLDER = "{{ post_href }}"
POST_SUMMARY_TITLE_PLACEHOLDER = "{{ post_title }}"
POST_SUMMARY_TEXT_PLACEHOLDER = "{{ post_summary_text }}"
INDEX_FILE_NAME = "index.html"

# read index template content
index_template_fo = open(_TEMPLATES_DIR + "/index.html")
index_template_content = index_template_fo.read()
index_template_fo.close()

index_posts_list = ""

# read post template content
post_template_fo = open(_TEMPLATES_DIR + "/post.html")
post_template_content = post_template_fo.read()
post_template_fo.close()

def get_post_data(file):
    fo = open(_POSTS_DIR + "/" + file)
    file_name = fo.name.split("/")[1].split(".")[0] + ".html"
    raw_content = fo.read()
    fo.close()

    content_splits = raw_content.split("---")
    meta = content_splits[1].splitlines()
    print("post meta section:", meta)
    datetime = meta[1].split(": ")[1]
    title = meta[2].split(": ")[1]
    content = content_splits[2]

    return {
        "file_name": file_name,
        "raw_content": content,
        "datetime": datetime,
        "title": title,
        "content": content
    }

def create_post(data):
    post_content = post_template_content.replace(POST_META_PLACEHOLDER, data["datetime"])
    post_content = post_content.replace(POST_TITLE_PLACEHOLDER, data["title"])
    post_content = post_content.replace(POST_CONTENT_PLACEHOLDER, data["content"])

    return post_content

# read post summary template
post_summary_template_fo = open(_TEMPLATES_DIR + "/post-summary.html")
post_summary_template_content = post_summary_template_fo.read()
post_summary_template_fo.close()

def create_post_summary(data):
    post_summary_content = post_summary_template_content.replace(POST_SUMMARY_META_PLACEHOLDER, data["datetime"])
    post_summary_content = post_summary_content.replace(POST_SUMMARY_HREF_PLACEHOLDER, POSTS_DIR + "/" + data["file_name"])
    post_summary_content = post_summary_content.replace(POST_SUMMARY_TITLE_PLACEHOLDER, data["title"])
    post_summary_content = post_summary_content.replace(POST_SUMMARY_TEXT_PLACEHOLDER, "") # TODO: add summary to post meta
    return post_summary_content

for subdir, dirs, files in os.walk(_POSTS_DIR):
    for file in files:
        post_data = get_post_data(file)
        # replace post content placeholder
        new_post_content = create_post(post_data)
        # write post
        new_post_fo = open(POSTS_DIR + '/' + post_data["file_name"], "w")
        new_post_fo.write(new_post_content)
        new_post_fo.close()
        index_posts_list += create_post_summary(post_data)

# replace index post list placeholder
index_content = index_template_content.replace(POSTS_LIST_PLACEHOLDER, index_posts_list)
# write index
index_fo = open(INDEX_FILE_NAME, "w")
index_fo.write(index_content)
index_fo.close()
