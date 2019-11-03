import json

import flask

from seo import get_seo

app = flask.Flask(__name__)


@app.route("/")
def home():
    return flask.render_template("home.html")


@app.route("/", methods=["POST"])
def home_form():
    url = flask.request.form["url"]
    return flask.redirect(flask.url_for(".seo", url=url))


@app.route("/seo/<path:url>")
def seo(url):
    data = get_seo(url)

    if flask.request.content_type == "application/json":
        return flask.jsonify(data)

    return flask.render_template("seo.html", data=data)

