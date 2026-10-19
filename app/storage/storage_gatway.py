import io
from storage import StorageService

from app.core.exception import StorageError, AppError

class Storage:
  def __init__(self, config):
    self.store = StorageService(config)

  def save(self, filename: str, file_bytes: bytes):
    try:
      return self.store.save(io.BytesIO(file_bytes), filename= filename)

    except Exception as e:
      raise StorageError(message= f"An error occurred while saving file '{filename}' {e}") from e

  def load(self, object_id: str) -> bytes:
    try:
      data = self.store.load(object_id)
      return data
    
    except Exception as e:
      raise StorageError(message= f"An error occurred while loading object '{object_id}' {e}") from e


  def get_metadata(self, object_id: str):
    try:
      return self.store.metadata(object_id)

    except Exception as e:
      raise AppError(f"An error occurred while getting metadata for object '{object_id}': {e}") from e

  def cleanup(self, interval):
    try:
      return self.store.start_cleanup(interval=interval)
    
    except Exception as e:
      raise AppError(f"Failed to initiate storage cleanup sequence: {e}") from e