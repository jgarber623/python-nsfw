import numpy
import os
import PIL.Image as Image

os.environ["GLOG_minloglevel"] = "2"

from caffe import Net
from caffe.io import load_image, Transformer
from io import BytesIO


def _process(bytes, *, net, transformer):
    """
    Process an image using a Caffe network and transformer.

    Parameters
    ----------
    bytes       : a resized image as a BytesIO object
    net         : an instance of caffe.Net
    transformer : an instance of caffe.io.Transformer

    Returns
    -------
    probabilities : an array of SFW and NSFW probabilities as floats
    """

    loaded_image = load_image(bytes)
    layers = ["prob"]

    H, W, _ = loaded_image.shape
    _, _, h, w = net.blobs["data"].data.shape

    h_off = int(max((H - h) / 2, 0))
    w_off = int(max((W - w) / 2, 0))

    cropped_image = loaded_image[h_off:h_off + h, w_off:w_off + w, :]
    transformed_image = transformer.preprocess("data", cropped_image)

    transformed_image.shape = (1,) + transformed_image.shape

    output = net.forward_all(blobs=layers, **{
        net.inputs[0]: transformed_image
    })

    return output[layers[0]][0].astype(float)


def _resize(image, size=(256, 256)):
    """
    Resize an image to match Yahoo's open_nsfw pretrained model.

    Parameters
    ----------
    image : a PIL ImageFile object
    size  : a (width, height) tuple

    Returns
    -------
    bytes : a resized image as a BytesIO object
    """

    if image.mode != "RGB":
        image = image.convert("RGB")

    resized_image = image.resize(size, resample=Image.BILINEAR)
    bytes = BytesIO()

    resized_image.save(bytes, format="JPEG")

    return bytes


def _static_file(name):
    """
    Return the path to a file included via `MANIFEST.in`.

    Parameters
    ----------
    name : a file name

    Returns
    -------
    path : an absolute filesystem path
    """
    return os.path.join(os.path.dirname(__file__), name)


def classify(
    image,
    model=_static_file("deploy.prototxt"),
    weights=_static_file("resnet_50_1by2_nsfw.caffemodel"),
):
    """
    Determine the probability that an image is SFW or NSFW.

    Parameters
    ----------
    image   : a PIL ImageFile object

    Keyword Arguments
    -----------------
    These arguments will default to the Yahoo OpenNSFW Defaults. If you have
    your own trained models, you may pass the path to the prototxt and
    caffemodel files.

    model   : a string path to a Caffe model file (e.g. deploy.prototxt)
    weights : a string path to a Caffe weights file (e.g. caffenet.caffemodel)

    Returns
    -------
    (sfw, nsfw) : a tuple with SFW and NSFW probabilities
    """

    net = Net(model, 1, weights=weights)

    transformer = Transformer({
        "data": net.blobs["data"].data.shape
    })
    # Move image channels to outermost
    transformer.set_transpose("data", (2, 0, 1))
    # Subtract the dataset-mean value in each channel
    transformer.set_mean("data", numpy.array([104, 117, 123]))
    # Rescale from [0, 1] to [0, 255]
    transformer.set_raw_scale("data", 255)
    # Swap channels from RGB to BGR
    transformer.set_channel_swap("data", (2, 1, 0))

    sfw, nsfw = _process(_resize(image), net=net, transformer=transformer)

    return (sfw, nsfw)
