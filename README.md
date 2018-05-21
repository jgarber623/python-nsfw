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

## Installation

python-nsfw may be installed using [pip](https://pip.pypa.io):

```python
pip3 install nsfw
```

## Usage

```python
import PIL.Image as Image

from nsfw import classify

image = Image.open("/path/to/image.jpg")
sfw, nsfw = classify(image)

print("SFW Probability: {}".format(sfw))
print("NSFW Probability: {}".format(nsfw))
```

## License

python-nsfw is freely available under the [MIT License](https://opensource.org/licenses/MIT). Use it, learn from it, fork it, improve it, change it, tailor it to your needs.

python-nsfw ships with copies of Yahoo's [open_nsfw Caffe models](https://github.com/yahoo/open_nsfw/tree/master/nsfw_model) (`nsfw/deploy.prototxt` and `nsfw/resent_50_1by2_nsfw.caffemodel`) which are licensed under the [BSD 2-Clause License](https://github.com/BVLC/caffe/blob/master/LICENSE).

[pypi]: https://pypi.org/project/nsfw
