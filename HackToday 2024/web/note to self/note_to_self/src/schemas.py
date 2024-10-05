from pydantic import BaseModel

class FileDownloadLegacy(BaseModel):
    filename: str
    path: str


class FileDownload(FileDownloadLegacy):
    filename: str
    path: str = './files/'

class User(BaseModel):
    name: str

class Note(BaseModel):
    content: str