import json
import requests

url = ""
try:
    url = os.environ["URL"]
except:
    pass

num_notification = 2



data_url = 'data/data.json'

def read_data(data_url, num_notification):
    with open (data_url, 'r') as data:
        jsn = json.load(data)
    keys = list(jsn.keys())
    for i in range(num_notification):
        ndata = jsn[keys[i]]
        send_notification(ndata, keys)



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



print(read_data(data_url, num_notification))