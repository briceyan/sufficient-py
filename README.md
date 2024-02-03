# sufficient

A framework for creating Frame apps in an intuitive and declarative manner.

[![PyPI - Version](https://img.shields.io/pypi/v/sufficient.svg)](https://pypi.org/project/sufficient)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sufficient.svg)](https://pypi.org/project/sufficient)

---

## Installation

```console
pip install sufficient
```

## Quick Start

The code below is from [frame-app-boilerplate]("https://github.com/briceyan/frame-app-boilerplate").

1. Create a Python project with the following directory structure.

```pre
api
└── index.py
frame
├── app.py
├── static
│   └── home.svg
└── templates
    └── foo.svg
```

2. Define your frame app in frame/app.py.

```python
from sufficient.frames import *


class App:
    name = "GM Universe"
    description = "A boilerplate for creating frame apps"
    image = "{uri}/static/home.svg"
    uri = "{uri}"
    start = "PageHome"


class PageHome:
    def view(self, action: Action, result: ActionResult):
        return SvgFile("home.svg")

    def btn_normal_button(self, action: Action):
        return "PageNext"

    def goto_redirect_button(self, action: Action):
        return "https://github.com/briceyan/frame-app-boilerplate"

    def input_input_text(self, action: Action):
        # wip
        pass


class PageNext:
    def view(self, action: Action, result: ActionResult):
        return SvgTemplate("foo.svg", title="PageNext", content="hello")

    def btn_prev(self, action: Action):
        return "PageHome"

    def btn_refresh(self, action: Action):
        return "PageNext"

```

3. In api/index.py, create routes as endpoints of your frame server.

```python

from flask import Flask, request, send_from_directory, redirect
import os
import io
import json
from sufficient.frames import FrameAppRunner
from frame import app as frame_app


app = Flask(__name__, instance_relative_config=True)

static_dir = os.path.abspath("frame/static")
templates_dir = os.path.abspath("frame/templates")
# data_dir = app.instance_path
data_dir = "/tmp/data"

runner = FrameAppRunner(frame_app, static_dir,
                        templates_dir, data_dir=data_dir)
try:
    os.makedirs(data_dir)
except OSError:
    pass


@app.route('/')
def frame_index():
    framelet = runner.start()
    return runner.gen_frame_html(framelet, request.host_url, og=True)


@app.route('/static/<string:path>')
def frame_static(path):
    return send_from_directory(static_dir, path)


@app.route('/view/<string:path>')
def frame_image(path):
    return send_from_directory(data_dir, path)


@app.route('/<string:page>/click', methods=['POST'])
def frame_click(page):
    tag, value = runner.click(page, request.json)
    if tag == "framelet":
        return runner.gen_frame_html(value, request.host_url)
    elif tag == "redirection":
        return redirect(value, code=302)

```

4. Run your app locally for testing

```console
python3 -m venv venv
source venv/bin/activate
pip install sufficient flask
python -m flask --app api.index run
```

5. Use ngrok to make your local server publically accessible

```console
ngrok http 5000 --scheme http,https
```

6. Validate your frame app

- https://warpcast.com/~/developers/frames

7. Deploy

The following instructions are assuming you are going to deploy on vercel. see https://vercel.com/docs/functions/serverless-functions/runtimes/python for more info.

create vercel.json with content:

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/api/index" }]
}
```

```bash
vercel deploy
```

## License

`sufficient` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
