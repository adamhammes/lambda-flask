import urllib.parse

import bs4
import requests


def _get_meta(soup, name, match_on="name"):
    tag = soup.find("meta", {match_on: name})
    return tag.get("content", None) if tag else None


def _get_host(url):
    return urllib.parse.urlparse(url).hostname if url else None


def _get_twitter(soup, original_url):
    if not _get_meta(soup, "twitter:card"):
        return None

    url = _get_meta(soup, "twitter:url")
    url_host = _get_host(url) or _get_host(original_url)

    return {
        "site": _get_meta(soup, "twitter:site"),
        "title": _get_meta(soup, "twitter:title"),
        "description": _get_meta(soup, "twitter:description"),
        "image": _get_meta(soup, "twitter:image"),
        "image_alt": _get_meta(soup, "twitter:image:alt"),
        "url": _get_meta(soup, "twitter:url"),
        "url_host": url_host,
    }


def _get_open_graph(soup, original_url):
    properties = ["url", "title", "description", "image", "type", "locale"]

    data = {
        prop: _get_meta(soup, "og:" + prop, match_on="property") for prop in properties
    }

    data["url_host"] = _get_host(data["url"]) or _get_host(original_url)
    return data


def get_seo(url):
    page = requests.get(url).content
    soup = bs4.BeautifulSoup(page, features="html.parser")

    return {
        "title": soup.title.get_text() if soup.title else "",
        "language": soup.html.attrs.get("lang", None),
        "description": _get_meta(soup, "description"),
        "twitter": _get_twitter(soup, url),
        "open_graph": _get_open_graph(soup, url),
    }
