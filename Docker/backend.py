import feedparser
import json
import requests
import re
import csv
import os
from summarizer import summarize
from bs4 import BeautifulSoup
from datetime import datetime


def get_path():
    for i in range(len(__file__)):
        if __file__[-i-1] == os.path.normcase("/"):
            return(str(__file__[0:-i]))
    return("")


def write_json_data(str, name):
    with open(get_path()+name, "w") as data:
        json.dump(str, data)


def write_csv_data(list, name):
    with open(get_path()+name, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(list)


url = ""
try:
    url = os.environ["URL"]
except:
    pass


def send_notification(data, id):
    text = "shortened-text"
    link = data["link"]
    if(len(data["unshortened-text"]) < len(data["shortened-text"])
            or len(data["unshortened-text"]) < 250):
        text = "unshortened-text"
    if len(url) > 8:
        link = url + "#" + id
    requests.post("https://ntfy.sh/Netz-Politik-News-Push",
                  data=data[text].encode("utf-8"),
                  headers={
                          "Title": data["title"].encode("utf-8"),
                          "Priority": "urgent",
                          "Tags": "warning",
                          "Click": link.encode("utf-8"),
                          "date": data["date"].encode("utf-8")
                      })


def convert_text(text, title):
    ar_short = summarize(title, text, count=2)
    return ''.join(str(e) for e in ar_short)


def feed_noname(url):
    try:
        with open(get_path()+"data.json", "r") as data:
            dict = json.loads(data.read())
    except:
        write_json_data({}, "data.json")
        dict = {}
    dict_old = dict.copy()
    blog_feed = feedparser.parse(url)
    for i in range(len(blog_feed.entries)):
        if blog_feed.entries[i].id.split("=")[1] not in dict.keys():
            beautifulsoup_object = BeautifulSoup(
                str(blog_feed.entries[i].content[0]["value"]),
                features="html.parser")
            if beautifulsoup_object.find("figure") is not None:
                beautifulsoup_object.find(
                    "figure").decompose()
            unshortened_text = beautifulsoup_object.get_text()
            beautifulsoup_object = BeautifulSoup(
                    str(blog_feed.entries[i].content[0]["value"]),
                    features="html.parser")
            img_source = beautifulsoup_object.find_all("img")
            img_list = []
            for img in img_source:
                img_list.append(img["src"])
            dict[blog_feed.entries[i].id.split("=")[1]] = {
                "title": blog_feed.entries[i].title,
                "unshortened-text": re.sub(r'(?<=[.,])(?=[^/s])', r' ',
                                           unshortened_text),
                "shortened-text": re.sub(r'(?<=[.,])(?=[^/s])', r' ',
                                         convert_text(unshortened_text,
                                                      blog_feed.entries[i].title)),
                "picture": img_list,
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
            send_notification(
                dict[date_sorted_list_keys[i][1]], date_sorted_list_keys[i][1])
        write_csv_data(date_sorted_list_keys, "sorted_keys.csv")
    write_json_data(dict, "data.json")


def everything():
    feed_noname("https://netzpolitik.org/feed")


everything()
