import os
import random
from aes import AES
import matplotlib.pyplot as plt


def flip_bit(x, index):
    byte_index = index // 8
    bit_index = index % 8
    mask = 1 << (7 - bit_index)

    byte_list = list(x)
    byte_list[byte_index] ^= mask
    y = bytes(byte_list)
    return y

def hamming_distance(a, b):
    distance = sum(bin(x ^ y).count('1') for x, y in zip(a, b))
    return distance

def aes_diffusion(num_round=None):
    plaintext = os.urandom(16)
    key = os.urandom(16)
    bit_to_flip = random.randint(0, 127)  # choose a random bit in 128-bit input
    flipped_plaintext = flip_bit(plaintext, bit_to_flip)

    aes = AES(key)
    ct1 = aes.partially_encrypt(plaintext, num_round)
    ct2 = aes.partially_encrypt(flipped_plaintext, num_round)

    distance = hamming_distance(ct1, ct2)
    return distance


def aes_confusion(num_round=None):
    plaintext = os.urandom(16)
    key = os.urandom(16)
    bit_to_flip = random.randint(0, 127)  # choose a random bit in 128-bit input
    flipped_key = flip_bit(key, bit_to_flip)

    aes1 = AES(key)
    aes2 = AES(flipped_key)

    ct1 = aes1.partially_encrypt(plaintext, num_round)
    ct2 = aes2.partially_encrypt(plaintext, num_round)

    distance = hamming_distance(ct1, ct2)
    return distance

