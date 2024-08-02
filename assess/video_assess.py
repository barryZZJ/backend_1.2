from typing import Literal

import numpy as np
np.float = float
np.int = int
import skvideo.io
import skvideo.measure.ssim

# TODO https://www.scikit-video.org/stable/measure.html
METHODS = Literal['ssim']


def calculate_video_ssim(vid1_path, vid2_path):
    vid1_frames = skvideo.io.vread(vid1_path, as_grey=True)
    vid2_frames = skvideo.io.vread(vid2_path, as_grey=True)
    similarity_indexes = skvideo.measure.ssim(vid1_frames, vid2_frames)
    similarity_index = np.average(similarity_indexes)
    return similarity_index


def video_assess(
    video_path: str,
    video_disturbed_path: str,
    method: METHODS,
    *args
):
    if method == 'ssim':
        return calculate_video_ssim(video_path, video_disturbed_path)
    else:
        raise NotImplementedError

if __name__ == '__main__':
    vid1 = r'..\src\videos\test.mp4'

    vid2 = r'..\src\videos\pixelate_region.mp4'
    print(video_assess(vid1, vid2, 'ssim'))
