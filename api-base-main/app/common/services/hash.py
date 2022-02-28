import hashlib
from loguru import logger

from sqlalchemy.sql.expression import false
from sqlalchemy.sql.sqltypes import Boolean

from common.services import encrypt

def hashed_string_md5(str_value:str) -> str:
    '''
    Devuelve el hash de una cadena en formato MD5
    @str_value cadena a codificar
    @return cadena codificada
    '''
    m = hashlib.md5()
    b: bytes = bytes(str(str_value), encoding='utf-8')
    m.update(b)
    return m.digest().decode('raw_unicode_escape')


def hash_renovacion_tar(str_value:str):
    '''
        Devuelve el hash de una cadena en formato hexdigest 
        @str_value cadena a codificar
        @return cadena codificada
    '''
    hash_object = hashlib.md5()
    hash_object.update(str_value.encode('utf-8'))
    valor =  hash_object.hexdigest()
    return valor


def hashed_string_pbkdf2(str_value: str, str_salt:str, algoritmo:str ='sha512') -> str:
    '''
    Devuelve el hash de una cadena en formato PBKDF2
    @str_value cadena a codificar
    @str_salt cadena aleatoria para incrementar seguridad
    @algoritmo algoritmo a usar para codificar la cadena
    @return cadena codificada
    '''
    iteraciones = 100*1000
    byte_salt = bytes.fromhex(str_salt)
    llave = hashlib.pbkdf2_hmac(algoritmo, str_value.encode('utf-8'), byte_salt, iteraciones)
    return llave.hex()


def compara_md5(original: str, challenge: str) -> Boolean:
    '''
    Compara 2 cadenas que han sido codificadas con el algoritmo MD5
    @original cadena original que se usa de referencia
    @challenge cadena contra la que se realiza la comparación
    @return Boolean indicando si las cadenas coinciden
    '''
    resultado = False
    total = min(len(original), len(challenge))
    hit = 0

    for char_pwd, char_comp in zip(original, challenge):
        if char_pwd == char_comp:
            hit += 1
    porcentaje = hit / total

    if porcentaje >= 0.75:
        resultado = True
    logger.debug("Porcentaje de coincidencia:" + str(porcentaje))
    return resultado

def calculate_salt(longitud=64):
    """
    Función de ayuda que calcula una llave criptográfica personal para cada cliente. Se utiliza
    al agregar nuevos clientes.
    @param longitud (Int): Número de bytes que la sal debe tener. Es diferente para cada
    algortimo de hash, el algoritmo actual es sha512 que utiliza una longitud de 64 bytes.
    """
    from os import urandom
    sal = urandom(longitud).hex()
    return sal
