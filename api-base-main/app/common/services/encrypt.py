from Crypto.Cipher import AES
from Crypto import Random
from typing import Optional
from loguru import logger
from hashlib import md5
import hashlib
import base64
import os

from common.config import ENCRYPT_KEY, ENCRYPT_IMG_KEY

key = hashlib.sha256(
    ENCRYPT_KEY.encode()
).digest()
bs = 32

def encrypt_file(input_file:str, output_file:str, password:str = ENCRYPT_IMG_KEY, key_length:int = bs):
    """
    Encripta archivos
    """
    with open(input_file, 'rb') as in_file, open(output_file, 'wb+') as out_file:
        block_size = AES.block_size
        salt = Random.new().read(block_size - len('Salted__'))
        key, iv = derive_key_and_iv(password, salt, key_length, block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        out_file.write('Salted__' + salt)
        finished = False
        while not finished:
            chunk = in_file.read(1024 * block_size)
            if len(chunk) == 0 or len(chunk) % block_size != 0:
                padding_length = (block_size - len(chunk) % block_size) or block_size
                chunk += padding_length * chr(padding_length)
                finished = True
            out_file.write(cipher.encrypt(chunk))

        in_file.close()
        out_file.close()

def decrypt_file(input_file:str, output_file:str, password:str = ENCRYPT_IMG_KEY, key_length:int = bs):
    """
    Desencripta archivos
    """
    with open(input_file, 'rb') as in_file, open(output_file, 'wb+') as out_file:
        bs = AES.block_size
        salt = in_file.read(bs)[len('Salted__'):]
        key, iv = derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        next_chunk = ''
        finished = False

        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
            if len(next_chunk) == 0:
                padding_length = ord(chunk[-1])
                chunk = chunk[:-padding_length]
                finished = True
            out_file.write(chunk)

        in_file.close()
        out_file.close()

def encrypt(raw:str)->str:
    if raw and raw !='':
        raw = raw.encode('utf8')  # encode to bytes here
        raw = __pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))
    else:
        return raw

def decrypt(value:Optional[str]) -> Optional[str]:
    if value is not None and value != '':
        value = base64.b64decode(value)
        iv = value[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return __unpad(cipher.decrypt(value[AES.block_size:])).decode('utf-8')
    else:
        return value

def __pad(s:str)->str:
    # pad with bytes instead of str
    logger.info(f'{s}: {type(s)}')
    logger.info(f'{(bs - len(s) % bs) * "a"}: {type((bs - len(s) % bs) * chr(bs - len(s) % bs))}')
    return s + (bs - len(s) % bs) * \
        chr(bs - len(s) % bs).encode('utf8')

def __unpad(s:str) -> str:
    return s[:-ord(s[len(s)-1:])]

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]