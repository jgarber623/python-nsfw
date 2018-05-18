import caffe
import numpy as np

from io import BytesIO
from PIL import Image


def _process(bytes, *, net, transformer):
    """
    """

    loaded_image = caffe.io.load_image(bytes)
    layers = ["prob"]

    H, W, _ = loaded_image.shape
    _, _, h, w = net.blobs["data"].data.shape

    h_off = int(max((H - h) / 2, 0))
    w_off = int(max((W - w) / 2, 0))

    cropped_image = loaded_image[h_off:h_off + h, w_off:w_off + w, :]
    transformed_image = transformer.preprocess("data", cropped_image)

    transformed_image.shape = (1,) + transformed_image.shape

    output = net.forward_all(blobs=layers, **{net.inputs[0]: transformed_image})

    return output[layers[0]][0].astype(float)


def _resize(image, size=(256, 256)):
    """
    """

    if image.mode != "RGB":
        image = image.convert("RGB")

    resized_image = image.resize(size, resample=Image.BILINEAR)
    bytes = BytesIO()

    resized_image.save(bytes, format="JPEG")

    return bytes


def classify(image, model, weights):
    """
    takes a PIL image, model (string, .prototxt), weights (string, .caffemodel)
    returns a tuple (sfw, nsfw)
    """

    net = caffe.Net(model, weights, caffe.TEST)

    transformer = caffe.io.Transformer({
        "data": net.blobs["data"].data.shape
    })
    # Move image channels to outermost
    transformer.set_transpose("data", (2, 0, 1))
    # Subtract the dataset-mean value in each channel
    transformer.set_mean("data", np.array([104, 117, 123]))
    # Rescale from [0, 1] to [0, 255]
    transformer.set_raw_scale("data", 255)
    # Swap channels from RGB to BGR
    transformer.set_channel_swap("data", (2, 1, 0))

    sfw, nsfw = _process(_resize(image), net=net, transformer=transformer)

    return (sfw, nsfw)
