import cv2
import base64
import numpy as np
from PIL import Image
from io import BytesIO


def imnormalize(img, mean, std, to_rgb=True):
    """Normalize an image with mean and std.

    Args:
        img (ndarray): Image to be normalized.
        mean (ndarray): The mean to be used for normalize.
        std (ndarray): The std to be used for normalize.
        to_rgb (bool): Whether to convert to rgb.

    Returns:
        ndarray: The normalized image.
    """
    img = img.copy().astype(np.float32)
    return imnormalize_(img, mean, std, to_rgb)


def imnormalize_(img, mean, std, to_rgb=True):
    """Inplace normalize an image with mean and std.

    Args:
        img (ndarray): Image to be normalized.
        mean (ndarray): The mean to be used for normalize.
        std (ndarray): The std to be used for normalize.
        to_rgb (bool): Whether to convert to rgb.

    Returns:
        ndarray: The normalized image.
    """
    # cv2 inplace normalization does not accept uint8
    assert img.dtype != np.uint8
    mean = np.float64(mean.reshape(1, -1))
    stdinv = 1 / np.float64(std.reshape(1, -1))
    if to_rgb:
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)  # inplace
    cv2.subtract(img, mean, img)  # inplace
    cv2.multiply(img, stdinv, img)  # inplace
    return img

def image_to_base64(image, format='PNG'):
    format_dict = {'JPG': 'JPEG', 'JPEG': 'JPEG', 'PNG': 'PNG'}
    output_buffer = BytesIO()
    image.save(output_buffer, format=format_dict[format.upper()])
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

def base64_to_image(base64_str, image_path=None):
    # print(base64_str)
    # base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_str)
    image_data = BytesIO(byte_data)
    image = Image.open(image_data)
    if image_path:
        image.save(image_path)
    return image

def bytes_to_image(img_bytes, image_path=None):
    # print(base64_str)
    # base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    image_data = BytesIO(img_bytes)
    image = Image.open(image_data)
    if image_path:
        image.save(image_path)
    return image

def image_to_bytes(image, format='PNG'):
    format_dict = {'JPG': 'JPEG', 'JPEG': 'JPEG', 'PNG': 'PNG'}
    output_buffer = BytesIO()
    image.save(output_buffer, format=format_dict[format.upper()])
    byte_data = output_buffer.getvalue()
    return byte_data