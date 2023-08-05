import secrets
from hashlib import blake2b
from string import ascii_letters, digits


ALPHABET = ascii_letters + digits


def make_random_string(length, alphabet=ALPHABET):
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def get_hash(text):
    h = blake2b()
    h.update(text.encode())
    return h.hexdigest()
