import string
import random


def gen_capture():
    s = string.ascii_letters+string.digits
    return "".join(random.sample(s, 4))


# print(gen_capture())