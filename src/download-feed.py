import feedparser
import json
from bs4 import BeautifulSoup


def write_json_data(str, path):
    with open(path, "w") as data:
        json.dump(str, data)


def feed_noname(url, path):
    try:
        with open(path, "r") as data:
            dict = json.loads(data.read())
    except:
        write_json_data({}, path)
        dict = {}
    blog_feed = feedparser.parse(url)
    for i in range(len(blog_feed.entries)):
        print(blog_feed.entries[i].keys())
        print(blog_feed.entries[i].summary)
        if not blog_feed.entries[i].id.split("=")[1] in dict.keys():
            dict[blog_feed.entries[i].id.split("=")[1]] = {
                "title": blog_feed.entries[i].title,
                "unshorted-text": BeautifulSoup(str(blog_feed.entries[i].content[0]["value"]), features="html.parser").get_text(),
                "author": blog_feed.entries[i].author,
                "link": blog_feed.entries[i].link,
                "date": blog_feed.entries[i].published
            }
        write_json_data(dict, path)


feed_noname("https://netzpolitik.org/feed", "unshortened.json")

"""
idea for all RSS urls...

import sys

if 1 < len(sys.argv):
    for i in range(len(sys.argv)-1):
        if sys.argv[i+1][:8] == "https://":
            feed_noname(sys.argv[i+1])
        else:
            print(sys.argv[i+1] + " isn't a url")"""
