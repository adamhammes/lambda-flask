import json

import bs4
import flask
import requests

app = flask.Flask(__name__)


@app.route("/")
def home():
    return flask.render_template("home.html")


@app.route("/", methods=["POST"])
def home_form():
    url = flask.request.form["url"]
    return flask.redirect(flask.url_for(".seo", url=url))


def get_meta(soup, name, match_on="name"):
    tag = soup.find("meta", {match_on: name})
    return tag.get("content", None) if tag else None


def get_twitter(soup):
    if not get_meta(soup, "twitter:card"):
        return None

    return {
        "site": get_meta(soup, "twitter:site"),
        "title": get_meta(soup, "twitter:title"),
        "description": get_meta(soup, "twitter:description"),
        "image": get_meta(soup, "twitter:image"),
        "image_alt": get_meta(soup, "twitter:image:alt"),
    }


def get_open_graph(soup):
    properties = ["url", "title", "description", "image", "type", "locale"]
    return {
        prop: get_meta(soup, "og:" + prop, match_on="property") for prop in properties
    }


def get_seo(page):
    soup = bs4.BeautifulSoup(page, features="html.parser")
    data = {}
    title_tag = soup.title
    data["title"] = title_tag.get_text() if title_tag else ""

    meta_description = soup.find("meta", {"name": "description"})
    data["description"] = meta_description["content"] if meta_description else ""

    data["language"] = soup.html.attrs.get("lang", None)
    data["twitter"] = get_twitter(soup)
    data["open_graph"] = get_open_graph(soup)
    return data


@app.route("/seo/<path:url>")
def seo(url):
    data = get_seo(requests.get(url).content)

    if flask.request.content_type == "application/json":
        return flask.jsonify(data)

    return flask.render_template("seo.html", json=json.dumps(data, indent=4))

