#!/usr/bin/python
# -*- coding: utf-8 -*-
import ssl
import socket
import os
from loguru import logger

from common.config import HSM_HOST, HSM_PORT

# SE DEFINEN VARIABLES A SER UTILIZADAS EN LA CREACION DEL SOCKET
# CAPath, Keyfile y certfile SON UTILIZADAS PARA EL CONTEXTO DEL SOCKET
# SI NO SE UTILIZAN CERTIFICADOS VALIDOS, LA CONEXION NO SERA ESTABLECIDA
# SE DECLARA LA RUTA ABSOLUTA HACIA LA LOCALIZACION DE LOS CERTIFICADOS DENTRO DEL SERVIDOR
#HOST, PORT = 'us01hsm01test.virtucrypt.com', 1102
HOST, PORT = HSM_HOST, int(HSM_PORT)
Keyfile="/etc/hsm/tls.key"
certfile="/etc/hsm/tls.crt"

def vexi_socket_certs(command_encrypted):
    try:
        # SE CREA EL SOCKET
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        # SE INGRESA EL CONTEXTO DE CONEXION QUE CONTIENE LOS CERTIFICADOS
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile, 
                                keyfile=Keyfile, 
                                password=None)
        # SE REALIZA EL WRAP SOCKET (CONVIERTE UN SOCKET NORMAL EN UN SSL SOCKET)
        wrapped_socket = context.wrap_socket(sock,                             
                                            server_side=False, 
                                            do_handshake_on_connect=True)
        # CONECTA Y REALIZA ENVIO DE DATOS (EL COMANDO ENCRIPTADO ES PROPORCIONADO POR vexiAPI2.py)
        wrapped_socket.connect((HOST, PORT))
        wrapped_socket.send(command_encrypted)     
        # REGRESA RESPUESTA DEL HSM A Y CIERRA SOCKET
        return(wrapped_socket.recv(2048*2))
    except Exception as err:
        logger.exception(str(err))
    finally:
        wrapped_socket.close()
    #NOTA: FALTA IMPLEMENTAR EL SOCKET EN MODO DAEMONICO PARA QUE SE MANTENGA ABIERTO Y ESCUCHANDO

def ao_echo():
    #SE COMPONE COMANDO: [AOECHO;AGVEXI RULES]
    #El valor anterior es un comando válido para la API de VirtuCrypt
    composed_command_echo_encrypted = str("[AOECHO;AGVEXI RULES;]").encode('utf8')
    
    #Se toma el comando compuesto en el paso anterior y se le envía al HSM por medio de un socket SSL:
    operation_echo_concluded = vexi_socket_certs(composed_command_echo_encrypted)
    
    return (operation_echo_concluded)



def ao_CPIN(AL,PAN,AW='1'):
    #SE COMPONE COMANDO: [AOECHO;AGVEXI RULES]
    #El valor anterior es un comando válido para la API de VirtuCrypt
    try:
        AK = PAN[-13:-1]
        composedCommandECHOEncrypted = str("[AOCPIN;AX"+os.getenv("HSM_PEK")+";AL"+AL+";AW"+AW+";AK"+AK+";]").encode('utf8') 
        #Se toma el comando compuesto en el paso anterior y se le envía al HSM por medio de un socket SSL:
        operationECHOConcluded = vexi_socket_certs(composedCommandECHOEncrypted).decode('utf8')
        #En en unarespuesta correcta debe de tenerse el valor GFY
    except Exception as err:
        logger.error("Error durante la ejecucion del comando {}".format(str(err)))
        #Se coloca el mensaje de error para validar el GFN, una respuesta correcta devuelte un GFN
        operationECHOConcluded = "[AOCPIN;BBS;GFN;AOERROR;]"
    return (operationECHOConcluded)

def ao_EPIN(AF,PAN,AW='1'):
    #SE COMPONE COMANDO: [AOECHO;AGVEXI RULES]
    #El valor anterior es un comando válido para la API de VirtuCrypt
    try:
        AK = PAN[-13:-1]
        #logger.error(str("[AOEPIN;AX"+os.getenv("HSM_PEK")+";AF"+AF+";AW"+AW+";AK"+AK+";]"))
        composedCommandECHOEncrypted = str("[AOEPIN;AX"+os.getenv("HSM_PEK")+";AF"+AF+";AW"+AW+";AK"+AK+";]").encode('utf8')
        #Se toma el comando compuesto en el paso anterior y se le envía al HSM por medio de un socket SSL:
        operationECHOConcluded = vexi_socket_certs(composedCommandECHOEncrypted).decode('utf8')
    except Exception as err:
        logger.error("Error durante la ejecucion del comando {}".format(str(err)))
        operationECHOConcluded = "[AOEPIN;BBS;GFN;AOERROR;]"
    return (operationECHOConcluded)
