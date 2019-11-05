from flask_cors import CORS
from flask import Flask, render_template, request, redirect, send_from_directory, json, jsonify, send_file
import os
from uuid import uuid4
import argparse
import time
import subprocess
import codecs
import requests
import json
import config
import traceback
import logging
from module import Module

logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=logging.INFO)

template_dir = os.path.abspath('views')
app = Flask(__name__, template_folder=template_dir)
CORS(app)

module = Module()


@app.route('/data/<path:path>')
def send_data(path):
    return send_from_directory('data', path)


@app.route("/api/v1/update", methods=["GET"])
def api_v1_update():
    check = module.update()
    if check:
        return jsonify(
            status=config.API_SUCCESS,
            msg="Success!"
        )
    else:
        return jsonify(
            status=config.API_ERROR,
            msg="Something went wrong!"
        )


@app.route("/api/v1/all", methods=["GET"])
def api_v1_all():
    return jsonify(
        status=config.API_SUCCESS,
        msg="Success!"
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    args = parser.parse_args()
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=False)
