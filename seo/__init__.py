import urllib.parse

import bs4
import requests


def get_meta(soup, name, match_on="name"):
    tag = soup.find("meta", {match_on: name})
    return tag.get("content", None) if tag else None


def get_host(url):
    return urllib.parse.urlparse(url).hostname if url else None


def get_twitter(soup, original_url):
    if not get_meta(soup, "twitter:card"):
        return None

    url = get_meta(soup, "twitter:url")
    url_host = get_host(url) or get_host(original_url)

    return {
        "site": get_meta(soup, "twitter:site"),
        "title": get_meta(soup, "twitter:title"),
        "description": get_meta(soup, "twitter:description"),
        "image": get_meta(soup, "twitter:image"),
        "image_alt": get_meta(soup, "twitter:image:alt"),
        "url": get_meta(soup, "twitter:url"),
        "url_host": url_host,
    }


def get_open_graph(soup, original_url):
    properties = ["url", "title", "description", "image", "type", "locale"]

    data = {
        prop: get_meta(soup, "og:" + prop, match_on="property") for prop in properties
    }

    data["url_host"] = get_host(data["url"]) or get_host(original_url)
    return data


def get_seo(url):
    page = requests.get(url).content
    soup = bs4.BeautifulSoup(page, features="html.parser")
    data = {}
    title_tag = soup.title
    data["title"] = title_tag.get_text() if title_tag else ""

    meta_description = soup.find("meta", {"name": "description"})
    data["description"] = meta_description["content"] if meta_description else ""

    data["language"] = soup.html.attrs.get("lang", None)
    data["twitter"] = get_twitter(soup, url)
    data["open_graph"] = get_open_graph(soup, url)
    return data
