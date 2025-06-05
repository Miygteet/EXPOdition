PROXY = {
    'http': 'http://0.0.0.0:8080',
    'https': 'https://0.0.0.0:8080'
    }
from flask import Flask, request, render_template_string, redirect
import requests
from urllib.parse import urlparse, urljoin

app = Flask(__name__)

BROWSER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Proxy Browser</title>
</head>
<body>
    <form method="get" action="/browse">
        <input type="text" name="url" placeholder="Enter URL" value="{{ url }}" style="width: 80%;">
        <button type="submit">Go</button>
    </form>
    <hr>
    {% if content %}
        {{ content|safe }}
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(BROWSER_TEMPLATE, content='', url='')

@app.route('/browse')
def browse():
    url = request.args.get('url', '')
    if not url.startswith('http'):
        url = 'http://' + url

    try:
        resp = requests.get(url)
        content = rewrite_links(resp.text, url)
    except Exception as e:
        content = f"<p>Error fetching {url}: {e}</p>"

    return render_template_string(BROWSER_TEMPLATE, content=content, url=url)

def rewrite_links(html, base_url):
    """Rewrite links to pass through the proxy."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.find_all(['a', 'link', 'script', 'img']):
        attr = 'href' if tag.name in ['a', 'link'] else 'src'
        if tag.has_attr(attr):
            original = tag[attr]
            tag[attr] = "/browse?url=" + urljoin(base_url, original)

    return str(soup)

if __name__ == '__main__':
    app.run(debug=True)

