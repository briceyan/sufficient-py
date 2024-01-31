# sufficient

[![PyPI - Version](https://img.shields.io/pypi/v/sufficient.svg)](https://pypi.org/project/sufficient)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sufficient.svg)](https://pypi.org/project/sufficient)

---

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install sufficient
```

## Quick Start

1. Clone this repository.

```console
cd SOME_DIR
git clone git@github.com:briceyan/sufficient-py.git
```

2. Change current directory to the gm example, install and start flask.

```console
cd sufficient-py/src/sufficient/examples/gm
python3 -m venv venv
source venv/bin/activate
pip install sufficient flask
python -m flask --app flaskr run
```

3. Use ngrok to make your local server publically accessible; this is quite useful during the development stage.

```console
ngrok http http://localhost:5000
```

4. Use validators to test the frame app

- https://warpcast.com/~/developers/frames
- https://www.opengraph.xyz/

## License

`sufficient` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
