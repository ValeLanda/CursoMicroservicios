from typing import Optional
from loguru import logger
import os

from common.model.domain.documento_drive import DocumentoDrive
from common.model.repositories.drive import DriveRepository
from common.model.domain.drive import Drive
def eliminar_documento(ruta_archivo:str):
    ERROR = """
        Archivo {} no fue borrado de local: {}
    """
    try:
        if os.path.isfile(ruta_archivo):
            os.remove(ruta_archivo)
            logger.info(f'Archivo {ruta_archivo} fue borrado de local')
        else:
            raise OSError('No es un archivo')
    except Exception as error:
        logger.exception(ERROR.format(ruta_archivo, str(error)))

def descargar_documento_drive(id_drive:str) -> Optional[DocumentoDrive]:
    ERROR = """
        Falló descarga de archivo {}: {}
    """
    try:
        extra_info = {}
        drive = Drive()
        repository = DriveRepository()

        credentials = repository.get_credentials(drive)
        file = credentials.CreateFile({'id': id_drive})

        name = file['title']
        encrypted_bytes = file.GetContentFile('', bytes=True)
        extra_info['fecha_ultima_modificacion'] = file.get('modifiedDate')[:10]

        return DocumentoDrive(name, encrypted_bytes, extra_info)
    except Exception as error:
        logger.exception(ERROR.format(id_drive, str(error)))
        return None
