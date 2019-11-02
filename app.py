import bs4
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/seo/<path:url>')
def seo(url):
    page = requests.get(url).content
    soup = bs4.BeautifulSoup(page)
    title = soup.title.get_text()
    return f"The page's title is '{title}'"

