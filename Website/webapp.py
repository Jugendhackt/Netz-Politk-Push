from flask import Flask
from flask import render_template
import json
import csv

port = 8080

app = Flask(__name__)


@app.route("/")
def index():
    idsToShow = []
    for line in csv.reader(open("../data/sorted_keys.csv", "r")):
        idsToShow.append(line[1])
        if len(idsToShow) == 10:
            break
    data = json.load(open("../data.json", "r"))
    return render_template("index.html", idsToShow=idsToShow, allArticles=data)


app.run(host="0.0.0.0", port=port)
