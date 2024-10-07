from random import SystemRandom
import string

from django.utils.text import slugify

def random_letters(size=5):
    return ''.join(SystemRandom().choices(
        string.ascii_lowercase+ string.digits, 
        k=size
    ))

def slugfy_new(text, size=5):
    return f'{slugify(text)}-{random_letters(size)}'


if __name__ == '__main__':
    print(slugfy_new('texto bla bla bla', 2))