import os


def ofd_desensitize(input_file, pages: list[int], output_file):
    input_file = os.path.abspath(input_file)
    output_file = os.path.abspath(output_file)
    JAR = os.path.join(os.path.dirname(__file__), 'ofd_desensitizer.jar')
    # JAR = 'E:/ofd_desensitizer.jar'
    CMD = f'java -jar {JAR} file -p {input_file} ofd {" ".join(map(str, pages))} -o {output_file}'
    return os.system(CMD)

if __name__ == '__main__':
    print(ofd_desensitize('../src/ofds/ofdtest.ofd', [1, 2], '../src/ofds/ofdtest_desensitized.ofd'))