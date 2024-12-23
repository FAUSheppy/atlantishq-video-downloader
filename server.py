#!/usr/bin/python3

import argparse
import flask
import sys
import subprocess
import os
import datetime
import werkzeug.utils

app = flask.Flask("Atlantis Downloader Interface")

@app.route('/get-list')
def get_video_list():
    '''Return a list of videos which should be downloaded'''

    secret = flask.request.args.get("secret")
    if not secret or secret != app.config["SECRET"]:
        return ("Invalid or missing secret", 401)

    # build response urls #
    response = []
    for url, status_dict in app.config["URLS"].items():
        if not status_dict.get("queried"):
            response.append(url)
            status_dict["queried"] = True

    return flask.jsonify(response)


@app.route('/submit-url', methods=["POST"])
def submit_url():

    secret = flask.request.args.get("secret")
    if not secret or secret != app.config["SECRET"]:
        return ("Invalid or missing secret", 401)

    # save submited url if it is not already in the list #
    url = flask.request.json.get("url")
    if not url:
        return ("Missing 'url' in json", 405)
    else:
        if url not in app.config["URLS"]:
            app.config["URLS"].update({ url : { "queried" : False } })
        else:
            return ("URL already in list", 409)


@app.route('/submit-file', methods=["POST"])
def submit_url():

    UPLOAD_DIR = "upload/"

    secret = flask.request.args.get("secret")
    if not secret or secret != app.config["SECRET"]:
        return ("Invalid or missing secret", 401)

    f = flask.request.files['file']
    fname = werkzeug.utils.secure_filename(f.filename)
    sfName = os.path.join(UPLOAD_DIR, fname)
    if not os.path.isfile(sfName):
        f.save(sfName)
        return ('Success', 204)
    else:
        return ('Conflicting File', 409)


@app.route('/', methods=["GET"])
def settings():

    secret = flask.request.args.get("secret")
    if not secret or secret != app.config["SECRET"]:
        return ("Invalid or missing secret", 401)


def create_app():

    secret = os.environ.get("APP_SECRET"):
    if not secret:
        print("Missing APP_SECRET in environment", file=sys.stderr)
        sys.exit(1)
    
    app.config["APP_SECRET"] = secret
    app.config["URLS"] = {}


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Simple Submission Downloader Interface',
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--interface', default="localhost", help='Interface on which to listen')
    parser.add_argument('--port', default="5000", help='Port on which to listen')
    args = parser.parse_args()

    with app.app_context():
        create_app()

    app.run(host=args.interface, port=args.port, debug=True)
