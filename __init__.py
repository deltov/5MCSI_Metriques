from flask import Flask, render_template, jsonify, request
from urllib.request import urlopen
from datetime import datetime
from collections import Counter
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/api/commits")
def commits_api():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    with urlopen(url) as response:
        commits_data = json.loads(response.read().decode("utf-8"))

    minutes = []
    for commit in commits_data:
        date_str = commit.get("commit", {}).get("author", {}).get("date")
        if date_str:
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minutes.append(dt.minute)

    counts = Counter(minutes)
    return jsonify(results=[{"minute": k, "count": v} for k, v in sorted(counts.items())])

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

@app.route("/commits/")
def commits():
    if request.headers.get("Accept") == "application/json":
        url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
        with urlopen(url) as response:
            commits_data = json.loads(response.read().decode("utf-8"))

        minutes = []
        for commit in commits_data:
            date_str = commit.get("commit", {}).get("author", {}).get("date")
            if date_str:
                dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                minutes.append(dt.minute)

        counts = Counter(minutes)
        return jsonify(results=[{"minute": k, "count": v} for k, v in sorted(counts.items())])

    return render_template("commits.html")

if __name__ == "__main__":
    app.run(debug=True)
