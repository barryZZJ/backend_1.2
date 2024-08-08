import pandas as pd

from .npeet import entropy_estimators as ee


def table_assess(
    table_path: str,
    table_disturbed_path: str,
):
    data = pd.read_csv(table_path, header=None).to_numpy(str)
    data_disturbed = pd.read_csv(table_disturbed_path, header=None).to_numpy(str)
    func = ee.entropyd

    h = func(data)
    h_disturbed = func(data_disturbed)

    h_diff = abs(h_disturbed - h)
    result = h_diff
    return result


if __name__ == '__main__':
    table_path = r'..\src\dataset\adult_small.csv'
    table_disturbed_path = r'..\src\dataset\adult_k3.csv'

    print(table_assess(table_path, table_disturbed_path))