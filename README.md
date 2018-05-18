# python-nsfw

**A Python package for analyzing images using [Caffe](https://github.com/BVLC/caffe) and [Yahoo's open_nsfw](https://github.com/yahoo/open_nsfw) models.**

[![PyPI](https://img.shields.io/pypi/v/nsfw.svg?style=for-the-badge)][pypi]
[![Python](https://img.shields.io/pypi/pyversions/nsfw.svg?style=for-the-badge)][pypi]

## Prerequisites

python-nsfw requires Python 3 and runs on Caffe-compatible systems.

### Caffe

If you're using macOS and [Homebrew](https://brew.sh), the easiest way to install [Caffe](https://github.com/BVLC/caffe) is with Homebrew:

```sh
brew install caffe
```

Alternatively, you could use a [Docker](https://www.docker.com) Linux image (e.g. [`debian:stretch-slim`](https://hub.docker.com/_/debian/)) and install the necessary dependencies:

```sh
apt update && apt install caffe-cpu python3 python3-pip wget
```

### Yahoo's open_nsfw Models

[Yahoo's open_nsfw models](https://github.com/yahoo/open_nsfw) may be downloaded directly from GitHub. These files can go anywhere on your system, but we'll use `/opt/open_nsfw`.

```sh
mkdir -p /opt/open_nsfw

wget -q -O - https://github.com/yahoo/open_nsfw/archive/master.tar.gz | tar xz -C /opt/open_nsfw --strip 1
```

## Installation

python-nsfw may be installed using [pip](https://pip.pypa.io):

```python
pip3 install nsfw
```

## Usage

```python
from nsfw import classify
from PIL import Image

image = Image.open("/path/to/image.jpg")
sfw, nsfw = classify(image, "/opt/open_nsfw/nsfw_model/deploy.prototxt", "/opt/open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel")

print("SFW Probability: {}".format(sfw))
print("NSFW Probability: {}".format(nsfw))
```

## License

python-nsfw is freely available under the [MIT License](https://opensource.org/licenses/MIT). Use it, learn from it, fork it, improve it, change it, tailor it to your needs.

[pypi]: https://pypi.org/project/nsfw
