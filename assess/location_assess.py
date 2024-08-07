import os
import argparse

import torch
import torch.nn.functional as F

from imagebind import data
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType

import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ori_position_path",
        type=str,
        default=None,
        help="Original text file path (in txt format)",
    )
    parser.add_argument(
        "--protect_position_path",
        type=str,
        default=None,
        help="Protected text file path (in txt format)",
    )
    args = parser.parse_args()

    assert os.path.exists(args.ori_position_path), "Original text file does not exist"
    assert os.path.exists(
        args.protect_position_path
    ), "Protected text file does not exist"


    with open(args.ori_position_path, "r") as f:
        ori_position_text = f.read()

    ori_position_number = [float(i) for i in ori_position_text.split()]

    with open(args.protect_position_path, "r") as f:
        protect_position_text = f.read()

    protect_position_number = [float(i) for i in protect_position_text.split()]

    location_assess(ori_position_number, protect_position_number)

def location_assess(ori_position_number: list[float], protect_position_number: list[float]):
    """
    The privacy protection ability (0 for no protection, 0.5 and larger for best)
    """
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    model = imagebind_model.imagebind_huge(pretrained=True)
    model.eval()
    model.to(device)

    position_text_input = [' '.join(map(str, ori_position_number)), ' '.join(map(str, protect_position_number))]

    inputs = {
        ModalityType.TEXT: data.load_and_transform_text(position_text_input, device),
    }
    with torch.no_grad():
        embeddings = model(inputs)

    position_text_embeddings = embeddings[ModalityType.TEXT]

    # 语意相似性
    cos_sim = (
        F.cosine_similarity(
            position_text_embeddings[0], position_text_embeddings[1], dim=0
        )
        .cpu()
        .numpy()
    )

    # 数值相似性
    ori_position_array = np.array(ori_position_number)
    protect_position_array = np.array(protect_position_number)

    assert ori_position_array.shape == protect_position_array.shape

    dot_product = np.dot(ori_position_array, protect_position_array)
    ori_norm = np.linalg.norm(ori_position_array)
    protect_norm = np.linalg.norm(protect_position_array)
    cos_similarity_array = dot_product / (ori_norm * protect_norm)
    cos_distance_number = 1 - cos_similarity_array

    # print(
    #     "The privacy protection ability (0 for no protection, 0.5 and larger for best): ",
    #     1 - (cos_sim + cos_distance_number) / 2,
    # )
    #
    return 1 - (cos_sim + cos_distance_number) / 2


if __name__ == "__main__":
    # main()
    os.chdir('..')
    print(location_assess([1.0, 2.0], [116.435842, 39.941626]))