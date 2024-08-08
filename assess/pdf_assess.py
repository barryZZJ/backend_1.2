import os
import argparse

import torch
import torch.nn.functional as F

from imagebind import data
from imagebind.models.imagebind_model import ModalityType

from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
)
import tempfile

from global_vars import Global


def save_images_to_temp_files(image_list):
    temp_files = []
    for image in image_list:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        image.save(temp_file, format="PNG")
        temp_file.close()
        temp_files.append(temp_file.name)
    return temp_files


def main():
    print("!!!! convert the ofd file to pdf format first !!!!")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ori_pdf_path",
        type=str,
        default=None,
        help="Original ofd file path (in pdf format)",
    )
    parser.add_argument(
        "--protect_pdf_path",
        type=str,
        default=None,
        help="Protected ofd file path (in pdf format)",
    )
    args = parser.parse_args()

    assert os.path.exists(args.ori_pdf_path), "Original ofd file does not exist"
    assert os.path.exists(args.protect_pdf_path), "Protected ofd file does not exist"
    pdf_assess(args.ori_pdf_path, args.protect_pdf_path)

def pdf_assess(ori_pdf_path, protect_pdf_path):
    """
    return: The privacy protection ability (0 for no protection, 0.5 and larger for best)
    """
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    model = Global.load_assess_model(device)

    ori_ofd_content = convert_from_path(ori_pdf_path)
    protect_ofd_content = convert_from_path(protect_pdf_path)

    ori_odf_paths = save_images_to_temp_files(ori_ofd_content)
    protect_odf_paths = save_images_to_temp_files(protect_ofd_content)

    # ofd_input = [ori_ofd_content, protect_ofd_content]

    inputs = {
        ModalityType.VISION: data.load_and_transform_vision_data(ori_odf_paths, device),
    }
    with torch.no_grad():
        embeddings = model(inputs)

    ori_ofd_embeddings = embeddings[ModalityType.VISION]

    inputs = {
        ModalityType.VISION: data.load_and_transform_vision_data(
            protect_odf_paths, device
        ),
    }
    with torch.no_grad():
        embeddings = model(inputs)

    protect_ofd_embeddings = embeddings[ModalityType.VISION]

    assert ori_ofd_embeddings[0].shape == protect_ofd_embeddings[0].shape

    # print(ori_ofd_embeddings)
    # print(protect_ofd_embeddings)

    # 语意相似性
    cos_sim = 0

    for i in range(len(ori_ofd_embeddings)):
        cos_sim += (
            F.cosine_similarity(ori_ofd_embeddings[i], protect_ofd_embeddings[i], dim=0)
            .cpu()
            .numpy()
        )

    # print(
    #     "The privacy protection ability (0 for no protection, 0.5 and larger for best): ",
    #     abs(1 - cos_sim),
    # )
    return abs(1 - cos_sim)


if __name__ == "__main__":
    main()
