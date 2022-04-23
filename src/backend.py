import feedparser
import json
import requests
from summarizer import summarize
from bs4 import BeautifulSoup
from datetime import datetime


def send_notification(data):
    requests.post("https://ntfy.sh/Netz-Politik-News-Push",
                  data=data["shorted-text"].encode("utf-8"),
                  headers={
                      "Title": data["title"].encode("utf-8"),
                      "Priority": "urgent",
                      "Tags": "warning",
                      "Click": data["link"].encode("utf-8"),
                      "date": data["date"].encode("utf-8")
                      })


def convert_text(text, title):
    ar_short = summarize(title, text, count=3)
    return ''.join(str(e) for e in ar_short)


def write_json_data(str, path):
    with open(path, "w") as data:
        json.dump(str, data)


def feed_noname(url):
    try:
        with open("unshortened.json", "r") as data:
            dict = json.loads(data.read())
    except:
        write_json_data({}, "unshortened.json")
        dict = {}
    dict_old = dict.copy()
    blog_feed = feedparser.parse(url)
    for i in range(len(blog_feed.entries)):
        if not blog_feed.entries[i].id.split("=")[1] in dict.keys():
            beautifulsoup_object = BeautifulSoup(
                str(blog_feed.entries[i].content[0]["value"]), features="html.parser")
            unshortened_text = beautifulsoup_object.get_text()
            dict[blog_feed.entries[i].id.split("=")[1]] = {
                "title": blog_feed.entries[i].title,
                "unshortened-text": unshortened_text,
                "shorted-text": convert_text(unshortened_text, blog_feed.entries[i].title),
                "picture": "beautifulsoup_object",
                "author": blog_feed.entries[i].author,
                "link": blog_feed.entries[i].link,
                "date": blog_feed.entries[i].published
            }
    if len(dict) > len(dict_old):
        date_sorted_list_keys = []
        for i in dict:
            date_sorted_list_keys.append((datetime.strptime(
                dict[i]["date"], '%a, %d %b %Y %H:%M:%S %z'), i))
        date_sorted_list_keys.sort(key=lambda item: item, reverse=True)
        for i in range(len(dict)-len(dict_old)):
            send_notification(dict[date_sorted_list_keys[i][1]])
        write_json_data(date_sorted_list_keys, "sorted_keys.json")
    write_json_data(dict, "unshortened.json")


def everything():
    feed_noname("https://netzpolitik.org/feed")


everything()
