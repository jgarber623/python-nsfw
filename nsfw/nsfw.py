import caffe
import numpy as np

from io import BytesIO
from PIL import Image


def _process_image(image, *, caffe_net, caffe_transformer, output_layers):
    """
    """

    if output_layers is None:
        output_layers = caffe_net.outputs

    loaded_image = caffe.io.load_image(image)

    H, W, _ = loaded_image.shape
    _, _, h, w = caffe_net.blobs['data'].data.shape

    h_off = int(max((H - h) / 2, 0))
    w_off = int(max((W - w) / 2, 0))

    cropped_image = loaded_image[h_off:h_off + h, w_off:w_off + w, :]
    transformed_image = caffe_transformer.preprocess('data', cropped_image)

    transformed_image.shape = (1,) + transformed_image.shape

    outputs = caffe_net.forward_all(blobs=output_layers, **{caffe_net.inputs[0]: transformed_image})

    return outputs[output_layers[0]][0].astype(float)


def _resize_image(image, size=(256, 256)):
    """
    """

    if image.mode != 'RGB':
        image = image.convert('RGB')

    resized_image = image.resize(size, resample=Image.BILINEAR)
    faux_image = BytesIO()

    resized_image.save(faux_image, format='JPEG')

    return faux_image


def classify(image, model_def, pretrained_model):
    """
    takes a PIL image, model_def (string, .prototxt), pretrained_model (string, .caffemodel)
    returns a tuple (sfw, nsfw)
    """

    caffe_net = caffe.Net(model_def, pretrained_model, caffe.TEST)

    caffe_transformer = caffe.io.Transformer({
        'data': caffe_net.blobs['data'].data.shape
    })
    # Move image channels to outermost
    caffe_transformer.set_transpose('data', (2, 0, 1))
    # Subtract the dataset-mean value in each channel
    caffe_transformer.set_mean('data', np.array([104, 117, 123]))
    # Rescale from [0, 1] to [0, 255]
    caffe_transformer.set_raw_scale('data', 255)
    # Swap channels from RGB to BGR
    caffe_transformer.set_channel_swap('data', (2, 1, 0))

    resized_image = _resize_image(image)
    sfw, nsfw = _process_image(resized_image, caffe_net=caffe_net, caffe_transformer=caffe_transformer, output_layers=['prob'])

    return (sfw, nsfw)
