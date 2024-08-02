from typing import Literal

import librosa
import librosa.feature
import librosa.util
import numpy as np
from scipy.spatial.distance import cosine

METHODS = Literal['cos']


def calc_audio_cosine_sim(aud1_path, aud2_path):
    audio1, sr1 = librosa.load(aud1_path)
    audio2, sr2 = librosa.load(aud2_path)

    common_length = max(len(audio1), len(audio2))

    audio1 = librosa.util.fix_length(audio1, size=common_length)
    audio2 = librosa.util.fix_length(audio2, size=common_length)

    chroma1 = librosa.feature.chroma_stft(y=audio1, sr=sr1)
    chroma2 = librosa.feature.chroma_stft(y=audio2, sr=sr2)

    flat_chroma1 = np.ravel(chroma1)
    flat_chroma2 = np.ravel(chroma2)

    similarity = 1 - cosine(flat_chroma1, flat_chroma2)

    return similarity


def audio_assess(
    audio_path: str,
    audio_disturbed_path: str,
    method: METHODS,
    *args
):
    if method == 'cos':
        return calc_audio_cosine_sim(audio_path, audio_disturbed_path)
    else:
        raise NotImplementedError


if __name__ == '__main__':
    vid1 = r'../src\audios\audiotest2.wav'

    vid2 = r'../src\audios\beeped2.wav'
    print(audio_assess(vid1, vid2, 'cos'))

