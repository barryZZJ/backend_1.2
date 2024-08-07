import os
import argparse

import torch
import torch.nn.functional as F

from imagebind import data
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType

import numpy as np


def calculate_normalized_l1_distance(array1, array2, max_value):
    # 计算L1距离
    l1_distance = np.sum(np.abs(array1 - array2))

    # 计算可能的最大L1距离
    max_l1_distance = len(array1) * max_value

    # 归一化L1距离
    normalized_l1_distance = l1_distance / max_l1_distance

    return normalized_l1_distance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ori_trace_path",
        type=str,
        default=None,
        help="Original text file path (in txt format)",
    )
    parser.add_argument(
        "--protect_trace_path",
        type=str,
        default=None,
        help="Protected text file path (in txt format)",
    )
    args = parser.parse_args()

    assert os.path.exists(args.ori_trace_path), "Original text file does not exist"
    assert os.path.exists(args.protect_trace_path), "Protected text file does not exist"

    with open(args.ori_trace_path, "r") as f:
        ori_trace_text = f.read()

    ori_trace_number = [float(i) for i in ori_trace_text.split()]

    with open(args.protect_trace_path, "r") as f:
        protect_trace_text = f.read()

    protect_trace_number = [float(i) for i in protect_trace_text.split()]

def trace_assess(ori_trace_number: list[(float, float)], protect_trace_number: list[(float, float)]):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    model = imagebind_model.imagebind_huge(pretrained=True)
    model.eval()
    model.to(device)

    # 数值相似性
    ori_trace_array = np.array(ori_trace_number).flatten()
    protect_trace_array = np.array(protect_trace_number).flatten()

    trace_text_input = [' '.join(ori_trace_array.astype(str)), ' '.join(protect_trace_array.astype(str))]

    inputs = {
        ModalityType.TEXT: data.load_and_transform_text(trace_text_input, device),
    }
    with torch.no_grad():
        embeddings = model(inputs)

    trace_text_embeddings = embeddings[ModalityType.TEXT]

    # 语意相似性
    cos_sim = (
        F.cosine_similarity(trace_text_embeddings[0], trace_text_embeddings[1], dim=0)
        .cpu()
        .numpy()
    )


    assert ori_trace_array.shape == protect_trace_array.shape

    dot_product = np.dot(ori_trace_array, protect_trace_array)
    ori_norm = np.linalg.norm(ori_trace_array)
    protect_norm = np.linalg.norm(protect_trace_array)
    cos_similarity_array = dot_product / (ori_norm * protect_norm)
    cos_distance_number = 1 - cos_similarity_array

    # 位置关联性
    ori_trace_number.sort()
    protect_trace_number.sort()
    sort_ori_trace = np.array(ori_trace_number)
    sort_protect_trace = np.array(protect_trace_number)
    location_relation = np.sum(np.abs(sort_ori_trace - sort_protect_trace))
    ori_trace_number.extend(protect_trace_number)
    max_value = max(ori_trace_number) * len(protect_trace_number)
    normlize_location_relation = location_relation / max_value

    result = 1 - (cos_sim + cos_distance_number + normlize_location_relation) / 3
    print(
        "The privacy protection ability (0 for no protection, 0.5 and larger for best): ",
        result,
    )
    return float(np.average(result))


if __name__ == "__main__":
    # main()
    os.chdir('..')
    tr1 = [(1.0, 2.0), (116.435842, 39.941626), (3.0, 4.0)]
    tr2 = [(1.0, 2.0), (116.43794199999999, 39.932226), (3.0, 4.0)]
    print(trace_assess(tr1, tr2))