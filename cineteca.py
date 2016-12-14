#!/usr/bin/env python3
from flask import Flask, render_template, send_from_directory
from os import listdir

app = Flask(__name__)


@app.route('/')
def root():
    return render_template("index.html",
                           videos=listdir("videos"))


@app.route('/<name>')
def serve_file(name):
    return send_from_directory('videos', name)


if __name__ == "__main__":
    app.run()
