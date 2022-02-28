from httplib2 import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from loguru import logger

from common.model.domain.drive import Drive

class DriveRepository:
    def get_credentials(self, drive:Drive) -> GoogleDrive:
        try:
            GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = drive.credentials_dir
            google_auth = GoogleAuth()
            google_auth.LoadCredentialsFile(drive.credentials_dir)

            if google_auth.credentials is None:
                google_auth.LocalWebserverAuth(port_numbers=[8092])
            elif google_auth.access_token_expired:
                google_auth.Refresh()
            else:
                google_auth.Authorize()

            google_auth.SaveCredentialsFile(drive.credentials_dir)
            credentials = GoogleDrive(google_auth)
            logger.debug('credenciales obtenidas exitosamente')

            return credentials
        except Exception as error:
            logger.exception('fallo en la obtención de credenciales')
            raise error
