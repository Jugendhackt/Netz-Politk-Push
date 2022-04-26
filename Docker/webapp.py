import json
import csv
import os
from flask import Flask
from flask import render_template


def webapp():
    port = 8080

    app = Flask(__name__)

    def get_path():
        for i in range(len(__file__)):
            if __file__[-i-1] == os.path.normcase("/"):
                return(str(__file__[0:-i]))
        return("")

    @app.route("/")
    def index():
        idsToShow = []
        for line in csv.reader(open(get_path()+"sorted_keys.csv", "r")):
            idsToShow.append(line[1])
            if len(idsToShow) == 10:
                break
        data = json.load(open(get_path()+"data.json", "r"))
        return render_template("index.html", idsToShow=idsToShow, allArticles=data)

    app.run(host="0.0.0.0", port=port)
