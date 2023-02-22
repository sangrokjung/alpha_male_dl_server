import base64
from PIL import Image
from io import BytesIO
import numpy as np
def load_img(img_url: str):
    img_d = base64.b64decode(img_url)
    img_out = Image.open(BytesIO(img_d))
    img_n = np.array(img_out)


def encoding(path):
    with open(path, 'rb') as img:
        base64_string = base64.b64encode(img.read())
    return base64_string

def decoding(b64):
    img = base64.b64decode(b64)
    img = Image.open(BytesIO(img))
    img.save('/Users/werther/alpha_male_Back/app/v1/sample.jpg')
    return img
