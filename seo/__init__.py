import urllib.parse

import bs4
import requests


def _schemafiy_url(url):
    """
    Adds a default scheme of `http` to the url if no scheme is present.
    Example input/output:
        hammes.io           ->  http://hammes.io
        https://google.com  ->  https://google.com (unchanged)
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        return "http://" + url
    return url


def _get_meta(soup, name, match_on="name"):
    tag = soup.find("meta", {match_on: name})
    return tag.get("content", None) if tag else None


def _get_host(url):
    return urllib.parse.urlparse(url).hostname if url else None


def _get_twitter(soup, original_url):
    url = _get_meta(soup, "twitter:url")
    url_host = _get_host(url) or _get_host(original_url)

    return {
        "card": _get_meta(soup, "twitter:card"),
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
    if not data["title"] and soup.title:
        data["title"] = soup.title.get_text()

    return data


def get_seo(url):
    page = requests.get(_schemafiy_url(url)).content
    soup = bs4.BeautifulSoup(page, features="html.parser")

    return {
        "title": soup.title.get_text() if soup.title else "",
        "language": soup.html.attrs.get("lang", None),
        "description": _get_meta(soup, "description"),
        "twitter": _get_twitter(soup, url),
        "open_graph": _get_open_graph(soup, url),
    }
