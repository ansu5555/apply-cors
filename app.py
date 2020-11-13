import json
import logging
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

unused_headers = (
    "User-Agent",
    "Accept",
    "Cache-Control",
    "Postman-Token",
    "Host",
    "Accept-Encoding",
    "Connection",
    "Content-Length",
)


@app.route("/apply-cors/<path:url>", methods=["POST"])
def cors_post(url):
    try:
        url = request.view_args.get("url")
        if "://" not in url:
            url = url.replace(":/", "://")
        request_headers = dict(request.headers)
        headers = {k: v for k, v in request_headers.items() if k not in unused_headers}
        data = json.dumps(request.json)

        resp = requests.post(url, data=data, headers=headers)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "failed"}), 400


@app.route("/apply-cors/<path:url>", methods=["GET"])
def cors_get(url):
    try:
        url = request.view_args.get("url")
        if "://" not in url:
            url = url.replace(":/", "://")
        request_headers = dict(request.headers)
        headers = {k: v for k, v in request_headers.items() if k not in unused_headers}
        data = json.dumps(request.json)

        resp = requests.get(url, data=data, headers=headers)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "failed"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
