import os
import argparse

import torch
import torch.nn.functional as F

from imagebind import data
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ori_csv_path",
        type=str,
        default=None,
        help="Original csv file path (in txt format)",
    )
    parser.add_argument(
        "--protect_csv_path",
        type=str,
        default=None,
        help="Protected csv file path (in txt format)",
    )
    args = parser.parse_args()

    assert os.path.exists(args.ori_csv_path), "Original csv file does not exist"
    assert os.path.exists(args.protect_csv_path), "Protected csv file does not exist"

    csv_assess(args.ori_csv_path, args.protect_csv_path)

def csv_assess(ori_csv_path, protect_csv_path):
    """The privacy protection ability (0 for no protection, 0.5 and larger for best)"""
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    model = imagebind_model.imagebind_huge(pretrained=True)
    model.eval()
    model.to(device)

    with open(ori_csv_path, "r") as f:
        ori_csv = f.read()
    with open(protect_csv_path, "r") as f:
        protect_csv = f.read()

    csv_input = [ori_csv, protect_csv]

    inputs = {
        ModalityType.TEXT: data.load_and_transform_text(csv_input, device),
    }
    with torch.no_grad():
        embeddings = model(inputs)

    csv_embeddings = embeddings[ModalityType.TEXT]

    # 语意相似性
    cos_sim = (
        F.cosine_similarity(csv_embeddings[0], csv_embeddings[1], dim=0).cpu().numpy()
    )

    print(
        "The privacy protection ability (0 for no protection, 0.5 and larger for best): ",
        1 - cos_sim,
    )
    return 1 - cos_sim

if __name__ == "__main__":
    main()
