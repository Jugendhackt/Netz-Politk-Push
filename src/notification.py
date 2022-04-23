import requests



def send_notification(data):
    requests.post("https://ntfy.sh/phil_alerts",
    data= data["unshorted-text"],
    headers={
        "Title": data["title"],
        "Priority": "urgent",
        "Tags": "warning,skull",
        "Click": data ["link"],
        "Id": data ["id"]
    })

Name= {
    "title"           : "Titel",
    "unshorted-text"  : "Blabla",
    "link"            : "https://*/*",
    "date"            : "",
    "id"              : "<replace(title, ' ', '-) + date>"
  }

send_notification(Name)