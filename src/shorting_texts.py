from summarizer import summarize
import json

with open ('Feed-to-unshortened-json/unshorted.json', 'r') as data:
    jsn = json.load(data)

def convert_text(text, title):
    return summarize(title, text, count = 2)

keys = list(jsn.keys())

def in_json(jsn):

    keys = list(jsn.keys())

print(convert_text(jsn[keys[0]]['unshorted-text'],jsn[keys[0]]['title']))





