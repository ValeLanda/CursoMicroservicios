class DocumentoDrive:
    def __init__(self, name:str, content:any, extra_info:dict):
        self.name:str = name
        self.content:any = content
        self.extra_info:dict = extra_info