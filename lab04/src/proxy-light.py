import argparse
from urllib.parse import urlparse

import requests as requests
from flask import Flask, request, jsonify, Response

app = Flask(__name__)


def write_log(path, status_code):
    with open("../logs", "a") as file:
        file.write(f"{path} {status_code}\n")


def get_host(url):
    return urlparse(url).netloc


@app.route('/<path:url>', methods=['GET'])
def proxy(url):
    try:
        referer = request.headers.get('referer')
        new_headers = {
            'User-Agent': 'python-requests/2.26.0',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*'
        }
        # new_headers["User-Agent"] = request.headers["User-Agent"]
        # я честно постаралась настроить хедеры так, чтобы new_headers = request.headers,
        # но если поставить строчку выше, то он попытается редиректнуть на страницу с https и вернет 302
        if referer is not None:
            domain = referer.replace(request.host_url, '')
            full_url = '%s://%s/%s' % (request.scheme, domain, url)
            new_headers.update({"Referer": full_url})
        else:
            full_url = '%s://%s' % (request.scheme, url)
        new_headers.update({"Host": get_host(full_url)})
        response = requests.get(full_url, params=request.args, allow_redirects=False,
                                headers=new_headers, data=request.data)

        write_log(full_url, response.status_code)
        headers = dict(response.raw.headers)

        def generate():
            for chunk in response.raw.stream(decode_content=False):
                yield chunk

        out = Response(generate(), headers=headers)
        out.status_code = response.status_code
        return response.content, response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('port_number')
    args = parser.parse_args()
    app.run(port=int(args.port_number))
