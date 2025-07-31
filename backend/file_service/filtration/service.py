from typing import List
from models.file import File
from .schemas import FileFilterParams

def filter_files(files: List[File], params: FileFilterParams) -> List[File]:
    if params.name:
        return [f for f in files if params.name.lower() in f.filename.lower()]
    if params.created_from:
        return [f for f in files if f.created_at >= params.created_from]
    if params.created_to:
        return [f for f in files if f.created_at <= params.created_to]
    if params.size_min is not None:
        return [f for f in files if f.size is not None and f.size >= params.size_min]
    if params.size_max is not None:
        return [f for f in files if f.size is not None and f.size <= params.size_max]
    if params.file_type:
        return [f for f in files if f.content_type == params.file_type or (params.file_type == 'folder' and f.content_type == 'folder')]
    return files
