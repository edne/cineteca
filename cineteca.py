#!/usr/bin/env python3
import os
from flask import Flask, render_template, send_from_directory
from imdbpie import Imdb

app = Flask(__name__)
imdb = Imdb()


def local_video(local_path, file_name):
    name = os.path.splitext(file_name)[0]
    title = name.split("(")[0]  # Film name (year)
    imdb_out = imdb.search_for_title(title)
    if imdb_out:
        video = imdb_out[0]
        video.update({"location": "{}/{}".format(local_path, file_name)})
        return video
    else:
        None


def list_videos(local_path):
    names = os.listdir(local_path)
    videos = map(lambda name: local_video(local_path, name), names)
    videos = filter(lambda x: x, videos)
    return videos


# TODO: member of a class and updated every get
#       or yielded by a generator with a local state
print("loading video list")
videos = {video["imdb_id"]: video
          for video in list_videos("videos")}
print("done")


@app.route('/')
def root():
    video_list = sorted(videos.values(), key=lambda v: v["title"])
    return render_template("index.html", videos=video_list)


@app.route('/<imdb_id>')
def serve_file(imdb_id):
    return send_from_directory(".", videos[imdb_id]["location"])


if __name__ == "__main__":
    app.run()
