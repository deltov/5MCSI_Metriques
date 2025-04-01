from flask import Flask, render_template, jsonify
from datetime import datetime
from urllib.request import urlopen
import requests
import json
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/contact/")
def contact_form():
    return render_template("contact.html")

@app.route("/commits")
def commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    data = response.json()

    minute_counts = {}
    for commit in data:
        try:
            date_str = commit["commit"]["author"]["date"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            minute = date_obj.strftime("%H:%M")
            if minute in minute_counts:
                minute_counts[minute] += 1
            else:
                minute_counts[minute] = 1
        except Exception:
            continue

    results = [{"minute": m, "count": c} for m, c in sorted(minute_counts.items())]
    return render_template("commits.html", commit_data=results)

if __name__ == "__main__":
    app.run(debug=True)
