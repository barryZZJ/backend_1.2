import re
import random
import pandas as pd


def number_desensitize(text: str):
    text = re.sub(r'\d', lambda d: str(random.randint(0, 9)), str(text))
    return text
    # return float(text) if '.' in text else int(text)


def table_desensitize(
    input_file: str,
    output_file: str,
):
    df = pd.read_csv(input_file, header=None)
    df = df.astype(str)
    for x in range(df.shape[0]):
        for y in range(df.shape[1]):
            item = df.iat[x, y]
            if str(item).isdecimal():
                item2 = number_desensitize(item)
                df.iat[x, y] = item2
    df.to_csv(output_file, index=False, header=False)
    return output_file


if __name__ == '__main__':
    table_desensitize('../src/upload/ori_table.csv', '../src/upload/protect_table.csv')