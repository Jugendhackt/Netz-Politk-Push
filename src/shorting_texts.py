from summarizer import summarize
import json

with open ('Feed-to-unshortened-json/unshortened.json', 'r') as data:
    jsn = json.load(data)

def convert_text(text, title):
    ar_short = summarize(title, text, count = 3)
    return ''.join(str(e) for e in ar_short)
    


keys = list(jsn.keys())

def in_json(jsn):
    keys = list(jsn.keys())

    for i in range(len(keys)):
        jsn[keys[i]]['shorted_text'] = str(convert_text(jsn[keys[i]]['unshorted-text'],jsn[keys[i]]['title']))
    return jsn

new_array = (in_json(jsn))

