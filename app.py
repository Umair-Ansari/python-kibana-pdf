from flask import Flask, jsonify, abort, make_response
from flask import send_file
import re

from constants import Constants
from index import SeleniumCrawler
from response import Response

app = Flask(__name__)
from flask import request


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("recieve post request")
        response = Response()
        request_object = request.json
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if (not re.match(regex, request_object.get("url", ""))):
            abort(make_response(jsonify(response.get_response(Constants.URL_NOT_FOUND, Constants.URL_NOT_FOUND)),response.get_code(Constants.URL_NOT_FOUND)))
        
        print("url is valid")
        return jsonify(SeleniumCrawler().get_page(url=request_object.get("url", "")))

    else:
        return send_file('out.pdf')

if __name__ == '__main__':
   #app.run(debug = True)
   app.run(host='0.0.0.0', port=5000, debug = True)
