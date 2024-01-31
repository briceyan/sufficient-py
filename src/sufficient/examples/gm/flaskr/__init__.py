from flask import Flask, send_file, request, send_from_directory
import os
import io
import json
from sufficient.frames import FrameAppRunner, ImageFile, ImageView
from frame import app as frame_app


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev', DATABASE=os.path.join(
        app.instance_path, 'flaskr.sqlite'))
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    runner = FrameAppRunner(
        frame_app, "https://b24ef6151e56.ngrok.app", temp_dir=app.instance_path)

    @app.route('/')
    def frame_index():
        frame_meta = runner.start()
        og_meta = runner.gen_og_meta()
        html = runner.gen_frame_html(frame_meta | og_meta)
        return html

    @app.route('/view/<string:path>', methods=["GET", "HEAD"])
    def frame_image(path):
        return send_from_directory(runner.temp_dir, path, mimetype="image/png")

    @app.route('/<string:page>/click', methods=['POST'])
    def frame_click(page):
        frame_meta = runner.click(page, request.json)
        html = runner.gen_frame_html(frame_meta)
        return html

    return app
