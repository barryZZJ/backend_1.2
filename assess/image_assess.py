from typing import Literal

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

from assess.utils.imageutils import prepare_image

# TODO
#  https://scikit-image.org/docs/stable/api/skimage.metrics.html
#  https://zhuanlan.zhihu.com/p/483401892
METHODS = Literal['ssim']


def calculate_image_ssim(img1_path, img2_path) -> float:
    '''[0,1] 越大越相似'''
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    img1, img2, isgrayscale = prepare_image(img1, img2)

    img1arr = np.array(img1)
    img2arr = np.array(img2)
    channel_axis = None if isgrayscale else -1
    similarity_index = ssim(img1arr, img2arr, data_range=255, channel_axis=channel_axis)
    return similarity_index


def image_assess(
    img_path: str,
    img_disturbed_path: str,
    method: METHODS,
    *args
):
    if method == 'ssim':
        return calculate_image_ssim(img_path, img_disturbed_path)
    else:
        raise NotImplementedError

if __name__ == '__main__':
    img1 = r'../src\images\lena.jpg'
    img2 = r'../src\images\region_gaussian_blurred_image.jpg'
    print(image_assess(img1, img2, 'ssim'))
