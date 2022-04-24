from flask import Flask
from flask import render_template
import json

port = 8080

app = Flask(__name__)


@app.route("/")
def index():
    data = json.load(open("../data.json", "r"))
    return render_template("index.html", articlesToShow=data)


app.run(host="0.0.0.0", port=port)
