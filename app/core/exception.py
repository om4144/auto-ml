class AppError(Exception):
  def __init__(self, message: str= "An application error occured."):
    self.message = message

    super.__init__(self.message)


class InvalidDatasetError(AppError):
  def __init__(self, message: str= "The provided dataset is invalid or corrupted."):
    super().__init__(message)

class StorageError(AppError):
  def __init__(self, message: str= "A storage or file system error occurred."):
    super().__init__(message)