from flask import Blueprint, send_file
import website.paths as p

static_sender = Blueprint("static_sender", __name__)

@static_sender.route("/icon/<string:filename>")
def send_icon(filename):
    path = p.ikonky_folder_path() / filename
    return send_file(path)
