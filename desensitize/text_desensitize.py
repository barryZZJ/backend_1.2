import random
import re


characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_!@#$%^&*()-=+"


def randomize_string(text: str, replace):
    return text.replace(replace, ''.join(random.choices(characters, k=len(replace))))


if __name__ == '__main__':
    print(randomize_string('hello my name is abc', 'abc'))
