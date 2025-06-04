@app.route('/browse')
def browse():
    target_url = request.args.get('url')

    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    # --- Configure your proxy here ---
    proxy_host = 'http://your-proxy-server:port'  # e.g., http://123.123.123.123:8080
    proxy_user = 'your_username'
    proxy_pass = 'your_password'

    proxies = {
        'http': proxy_host,
        'https': proxy_host,
    }

    auth = (proxy_user, proxy_pass) if proxy_user and proxy_pass else None

    try:
        response = requests.get(target_url, proxies=proxies, auth=auth)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Rewrite links to go through proxy
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
