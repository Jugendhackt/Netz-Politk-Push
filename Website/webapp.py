from flask import Flask
from flask import render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    # data = json.load(open('samplearticles.json', 'r'))
    articlesToShow = [
        {
            "id": "1",
            "headline": "Breakiiiing News",
            "text": "Hello World! Lorem ipsum...",
            "url": "https://netzpolitik.org",
        },
        {
            "id": "2",
            "headline": "Breakiiiing News 2",
            "text": "Hello World! Lorem ipsum...",
            "url": "https://netzpolitik.org",
        }
    ]
    return render_template("index.html", articlesToShow=articlesToShow)

app.run(host="0.0.0.0", port=1929)
