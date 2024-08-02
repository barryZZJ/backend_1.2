import os
from typing import Callable

import pandas as pd


def get_spans(df, partition, categorical, scale=None):
    spans = {}
    for column in df.columns:
        if column in categorical:
            span = len(df[column][partition].unique())
        else:
            span = df[column][partition].max() - df[column][partition].min()
        if scale is not None:
            span = span / scale[column]
        spans[column] = span
    return spans


def split(df, partition, column, categorical):
    dfp = df[column][partition]
    if column in categorical:
        values = dfp.unique()
        lv = set(values[:len(values) // 2])
        rv = set(values[len(values) // 2:])
        return dfp.index[dfp.isin(lv)], dfp.index[dfp.isin(rv)]
    else:
        median = dfp.median()
        dfl = dfp.index[dfp < median]
        dfr = dfp.index[dfp >= median]
        return (dfl, dfr)


def is_k_anonymous(k=3):
    def is_k_anonymous_inner(df, partition, sensitive_column):
        if len(partition) < k:
            return False
        return True

    return is_k_anonymous_inner


def partition_dataset(df, feature_columns, sensitive_column, scale, is_valid: Callable, categorical):
    finished_partitions = []  # 初始化一个列表，用于存储已完成的分区
    partitions = [df.index]  # 初始化分区列表，开始时包含整个数据集的索引
    # df['partition'] = -1  # 在df中添加一个新列，用于存储分区索引，初始值设为-1表示未分配

    partition_id = 0  # 初始化分区ID，用于标识每个分区
    while partitions:  # 当还有分区需要处理时，循环继续
        partition = partitions.pop(0)  # 从分区列表中取出一个分区进行处理
        spans = get_spans(df[feature_columns], partition, scale)  # 计算当前分区中每个特征的跨度

        for column, span in sorted(spans.items(), key=lambda x: -x[1]):  # 按特征跨度降序排序，优先处理跨度大的特征
            lp, rp = split(df, partition, column, categorical)  # 将当前分区基于特征列进行分割，得到两个子分区

            if not is_valid(df, lp, sensitive_column) or not is_valid(df, rp, sensitive_column):  # 检查两个子分区是否都满足有效性条件
                continue  # 如果任一子分区不满足条件，跳过当前特征，尝试下一个特征

            partitions.extend((lp, rp))  # 如果两个子分区都满足条件，将它们添加到分区列表中，以便后续处理
            break  # 成功分割当前分区后，跳出循环，处理下一个分区
        else:
            # 如果当前分区无法进一步有效分割，将其添加到已完成分区列表
            finished_partitions.append(partition)
            partition_id += 1  # 更新分区ID，为下一个分区使用

    return finished_partitions  # 返回所有已完成的分区

def agg_categorical_column(series):
    return '~'.join(sorted(series.unique()))


def agg_numerical_column(series):
    return f'{series.min()}~{series.max()}'


def build_anonymized_dataset(df, partitions, feature_columns, sensitive_column, categorical, max_partitions=None):
    aggregations = {}  # 初始化聚合函数字典
    for column in feature_columns:  # 遍历特征列和敏感列
        if column in categorical:  # 如果列是分类数据
            aggregations[column] = agg_categorical_column  # 使用类别型聚合函数
        else:  # 如果列是数值数据
            aggregations[column] = agg_numerical_column  # 使用数值型聚合函数

    anonymized_df: pd.DataFrame = df.copy()

    for i, partition in enumerate(partitions):  # 遍历所有分区
        if i % 100 == 1:
            print("Finished {} partitions...".format(i))
        if max_partitions is not None and i > max_partitions:
            break
        grouped_columns: pd.Series = df.loc[partition].agg(aggregations, squeeze=False)
        # 将聚合结果更新回df的对应分区
        # 如果是Series，直接使用
        for column in grouped_columns.index:
            anonymized_df[column] = anonymized_df[column].astype(type(grouped_columns[column]))
            anonymized_df.loc[partition, column] = grouped_columns[column]

    return anonymized_df


def read_dataset(name):
    if name == 'adult':
        categorical = {
            'workclass',
            'education',
            'marital-status',
            'occupation',
            # 'relationship',
            'race',
            'sex',
            'native-country',
            'income'
        }

        df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "adultdataset/adult.drop_with_id_lesscol.csv"),
                         sep=",", header=0, index_col=False,
                         engine='python')
        feature_columns = ['age','workclass','education','marital-status','race','sex','native-country']
        sensitive_column = 'occupation'
    else:
        raise NotImplementedError()

    for name in categorical:
        df[name] = df[name].astype('category')

    return df, feature_columns, sensitive_column, categorical


def do_k_anonymity(df, feature_columns, sensitive_column, categorical, k):
    full_spans = get_spans(df, df.index, categorical)
    finished_partitions = partition_dataset(df, feature_columns, sensitive_column, full_spans, is_k_anonymous(k),
                                            categorical)
    dfn = build_anonymized_dataset(df, finished_partitions, feature_columns, sensitive_column, categorical)
    return dfn


