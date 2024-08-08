import os
import argparse

import torch
import torch.nn.functional as F

from imagebind import data
from imagebind.models.imagebind_model import ModalityType

from global_vars import Global


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ori_text_path",
        type=str,
        default=None,
        help="Original text file path (in txt format)",
    )
    parser.add_argument(
        "--protect_text_path",
        type=str,
        default=None,
        help="Protected text file path (in txt format)",
    )
    args = parser.parse_args()

    assert os.path.exists(args.ori_text_path), "Original text file does not exist"
    assert os.path.exists(args.protect_text_path), "Protected text file does not exist"

    with open(args.ori_text_path, "r") as f:
        ori_text = f.read()
    with open(args.protect_text_path, "r") as f:
        protect_text = f.read()

    text_assess(ori_text, protect_text)

def text_assess(ori_text, protect_text):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    model = Global.load_assess_model(device)

    text_input = [ori_text, protect_text]

    inputs = {
        ModalityType.TEXT: data.load_and_transform_text(text_input, device),
    }
    with torch.no_grad():
        embeddings = model(inputs)

    text_embeddings = embeddings[ModalityType.TEXT]

    # 语意相似性
    cos_sim = (
        F.cosine_similarity(text_embeddings[0], text_embeddings[1], dim=0).cpu().numpy()
    )

    # print(
    #     "The privacy protection ability (0 for no protection, 0.5 and larger for best): ",
    #     1 - cos_sim,
    # )
    return 1 - cos_sim


if __name__ == "__main__":
    # main()
    os.chdir('..')
    print(text_assess("hello my name is john", "hello my name is allen"))
    print(text_assess("hahahahahh", "prtected words"))