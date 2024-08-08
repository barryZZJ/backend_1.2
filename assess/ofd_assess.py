import torch
import torch.nn.functional as F

from imagebind import data
from imagebind.models.imagebind_model import ModalityType

import tempfile

from global_vars import Global
from global_utils import ofd_to_img


def save_images_to_temp_files(image_list):
    temp_files = []
    for image in image_list:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        image.save(temp_file, format="PNG")
        temp_file.close()
        temp_files.append(temp_file.name)
    return temp_files


def ofd_assess(ori_ofd_path, protect_ofd_path):
    """
    return: The privacy protection ability (0 for no protection, 0.5 and larger for best)
    """
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    ori_ofd_content = ofd_to_img(ori_ofd_path)
    protect_ofd_content = ofd_to_img(protect_ofd_path)

    ori_ofd_paths = save_images_to_temp_files(ori_ofd_content)
    print(ori_ofd_paths)
    protect_ofd_paths = save_images_to_temp_files(protect_ofd_content)
    print(protect_ofd_paths)

    # ofd_input = [ori_ofd_content, protect_ofd_content]
    model = Global.load_assess_model(device)

    inputs = {
        ModalityType.VISION: data.load_and_transform_vision_data(ori_ofd_paths, device),
    }
    with torch.no_grad():
        embeddings = model(inputs)

    ori_ofd_embeddings = embeddings[ModalityType.VISION]

    inputs = {
        ModalityType.VISION: data.load_and_transform_vision_data(
            protect_ofd_paths, device
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
    print(ofd_assess(
        "src/upload/ori_ofd.ofd",
        "src/upload/protect_ofd.ofd",
    ))
