from typing import Literal

import numpy as np
import pandas as pd
# import torch


def load_input(
    input_type: Literal['csv', 'model', 'picture'],
    *args,
    **kwargs,
):
    """
    若 input_type == 'csv'：
        args 与 kwargs 将传入pd.read_csv，args的第一个参数应为csv文件路径。数据表应包含两列，第一列为原数据，第二列为加噪后数据。
        返回两个numpy数组，分别对应第一列数据和第二列数据。
    若 input_type == 'model'：
        args 前两个参数为要对比的两个pytorch模型的参数的pkl文件的路径，第三、四个参数为这两个参数对应的模型本身，均为torch.nn.Module对象。
        返回两个torch.nn.Module对象。
    若 input_type == 'picture'：
        args 为要对比的两张图片的路径。
        返回两个PIL.Image.Image对象。
    """
    if input_type == 'csv':
        df = pd.read_csv(*args, **kwargs)
        df.dropna(inplace=True)
        return np.asarray(df.iloc[:, 0]), np.asarray(df.iloc[:, 1])
    # elif input_type == 'model':
    #     path = args[0]
    #     module = args[2]  # type: torch.nn.Module
    #     path_disturbed = args[1]
    #     module_disturbed = args[3]  # type: torch.nn.Module
    #     return load_model_by_path(path, module), load_model_by_path(path_disturbed, module_disturbed)
    # elif input_type == 'picture':
    #     return load_picture_by_path(args[0]), load_picture_by_path(args[1])
    else:
        raise NotImplementedError

