from common.config import DRIVE_DIR_CREDENTIALS, DRIVE_FOLDER_SHARED, DRIVE_ID_SHARED
class Drive:
    def __init__(
        self,
        id_shared:str = DRIVE_ID_SHARED,
        id_folder_shared:str = DRIVE_FOLDER_SHARED,
        credentials_dir:str = DRIVE_DIR_CREDENTIALS
    ):
        self.id_shared:str = id_shared
        self.id_folder:str = id_folder_shared
        self.credentials_dir:str = credentials_dir
        self.credentials:any