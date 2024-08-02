import pandas as pd

from .k_anonymity_master import do_k_anonymity


def csv_desensitize(input_file, k, QI_INDEX: list[int], SA_INDEX: int, output_file: str):
    df_before = pd.read_csv(input_file, header=0, index_col=False, engine='python')

    categorical_list = list(
        col for col in df_before.columns if df_before.dtypes[col] == 'object'
    )
    categorical = set(categorical_list)
    df_before[categorical_list] = df_before[categorical_list].astype('category')

    SA_NAME = df_before.columns[SA_INDEX]

    feature_columns = df_before.columns[QI_INDEX]
    sensitive_column = SA_NAME

    df_after = do_k_anonymity(df_before, feature_columns, sensitive_column, categorical, k)

    df_after.to_csv(output_file, index=False)

if __name__ == '__main__':
    csv_desensitize('../../src/dataset/adult_small.csv', 3, [0, 1, 2, 3, 4, 5, 6, 7], 8, '../../src/dataset/adult_k3.csv')