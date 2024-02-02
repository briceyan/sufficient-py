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

Code snippets here are excerpted from `gm-universe` under repo [frame-app-examples](https://github.com/briceyan/frame-app-examples), you may also want to check it.

1. Create a python project with a directory structure looks like this.

```pre
api
└── index.py
frame
├── app.py
├── static
│   ├── features.png
│   ├── home.png
│   ├── howitworks.png
│   ├── howitworks_deploy.png
│   ├── howitworks_programming.png
│   └── unexpected.png
└── templates
    ├── features.svg
    ├── features_casters.svg
    ├── features_chaindata.svg
    └── features_reactions.svg
```

2. Define your frame app in frame/app.py.

```python
from sufficient.frames import *


class App:
    name = "GM Universe"
    description = "Greetings from your first frame app using sufficient-py"
    image = "{uri}/static/home.png"
    uri = "{uri}"
    start = "PageHome"


class PageHome:
    def view(self, action: Action, result: ActionResult):
        return ImageFile("home.png")

    def btn_explore(self, action: Action):
        return "PageFeatures"


class PageFeatures:
    def view(self, action: Action, result: ActionResult):
        if "PageHome.btn_explore" == action.source:
            return ImageFile("features.png")
        elif "PageFeatures.btn_casters" == action.source:
            return SvgTemplate("features_casters.svg", result)
        elif "PageFeatures.btn_reactions" == action.source:
            return SvgTemplate("features_reactions.svg", result)
        elif "PageFeatures.btn_chain_data" == action.source:
            return SvgTemplate("features_chaindata.svg", result)
        else:
            return ImageFile("unexpected.png")

    def btn_casters(self, action: Action):
        c = FarcasterClient()
        users = c.neynar_get_users_bulk([action.actor, action.caster])
        actor_pfp = users[0]["pfp_url"]
        actor_name = users[0]["display_name"]
        caster_pfp = users[1]["pfp_url"]
        caster_name = users[1]["display_name"]
        return "PageFeatures", ActionResult(actor_name=actor_name,
                                            actor_pfp=actor_pfp,
                                            caster_name=caster_name,
                                            caster_pfp=caster_pfp)

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
ngrok http http://localhost:5000
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
