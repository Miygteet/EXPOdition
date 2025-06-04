from flask import Flask, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h2>Simple Proxy Browser</h2>
        <form action="/browse" method="get">
            <input type="text" name="url" placeholder="https://example.com" size="50"/>
            <input type="submit" value="Go"/>
        </form>
    '''

@app.route('/browse')
def browse():
    target_url = request.args.get('url')

    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    try:
        response = requests.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Rewrite all links to go through the proxy
        for tag in soup.find_all(['a', 'link', 'script', 'img']):
            attr = 'href' if tag.name in ['a', 'link'] else 'src'
            if tag.has_attr(attr):
                new_url = urljoin(target_url, tag[attr])
                if tag.name == 'a':
                    tag[attr] = url_for('browse', url=new_url)
                else:
                    tag[attr] = new_url

        return str(soup)
    except Exception as e:
        return f"<h3>Error:</h3><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True)
