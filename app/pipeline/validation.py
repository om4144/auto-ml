import io
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
from pandas.errors import EmptyDataError

from app.core.exception import InvalidDatasetError

class DatasetReader:
  def __init__(self, file_bytes: bytes, filename: str):
    self.file_bytes = io.BytesIO(file_bytes)
    self.filename = filename

    # finding file extension
    suffixs = Path(self.filename).suffixes
    self.file_ext = "".join(suffixs).lower()


  def read_file(self) -> pd.DataFrame:
    readers = {
      ".csv": pd.read_csv,
      ".xlsx": pd.read_excel,
      ".xls": pd.read_excel,
      ".json": pd.read_json,
      ".tsv": pd.read_csv,
    }

    try:
      if self.file_ext in readers.keys():
        if self.file_ext == ".tsv":
          return readers[self.file_ext](self.file_bytes, sep= "\t")
        
        return readers[self.file_ext](self.file_bytes)

      else:
        raise InvalidDatasetError(
          message= f"Invalid extension({self.file_ext}) for a Dataset"
        )

    except EmptyDataError:
      raise InvalidDatasetError(
        message= f"Given dataset({self.filename}) is empty."
      )

    except Exception as e:
      raise InvalidDatasetError(
        message= f"An unexcepted error occured: {e}"
      )


class Validater(DatasetReader):
  def __init__(self, config: Dict[str, Any]):
    self.target = config.get("target", None)
    self.filename = config.get("filename", None)

    super().__init__(
      file_bytes= config.get("file_bytes", None), 
      filename= self.filename
    )

    self.df: pd.DataFrame = super().read_file()

  def validate_dataset(self) -> Tuple[bool, pd.DataFrame]:
    rows = self.df.shape[0]
    col = set(self.df.columns.to_list())

    checks = [
      (lambda: rows < 100, f"Dataset({self.filename}) doesn't have enough row's"),
      (lambda: len(col) < 3, f"Dataset({self.filename}) needs at least 3 uniqur columns"),
      (lambda: self.target not in col, f"Dataset({self.filename}) doesn't have '{self.target}' columns"),
      (lambda: self.df[self.target].nunique() <= 1, f"{self.target} column needs more than one unique value")
    ]

    error = next((msg for exp, msg in checks if exp()), None)

    if error is not None:
      raise InvalidDatasetError(message= error)

    return (True, self.df)