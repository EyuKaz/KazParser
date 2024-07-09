import csv
import json
from typing import Generator, Dict, Union, Optional
import chardet
from .validators import SchemaValidator

class Omniparser:
    def __init__(self, 
                 filepath: str, 
                 delimiter: str = 'auto',
                 quotechar: str = '"',
                 has_header: bool = True):
        self.filepath = filepath
        self.detected_encoding = self._detect_encoding()
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.has_header = has_header
        self._validate_params()

    def _detect_encoding(self) -> str:
        with open(self.filepath, 'rb') as f:
            result = chardet.detect(f.read(1024*1024))
        return result['encoding']

    def _detect_delimiter(self) -> str:
        with open(self.filepath, 'r', encoding=self.detected_encoding) as f:
            sample = f.read(2048)
            possible_delims = [',', '\t', ';', '|']
            counts = {d: sample.count(d) for d in possible_delims}
            return max(counts.items(), key=lambda x: x[1])[0]

    def stream(self, 
               batch_size: int = 1000,
               transform: callable = None) -> Generator:
        delimiter = self.delimiter if self.delimiter != 'auto' else self._detect_delimiter()
        
        with open(self.filepath, 'r', encoding=self.detected_encoding) as f:
            reader = csv.reader(f, delimiter=delimiter, quotechar=self.quotechar)
            
            if self.has_header:
                headers = next(reader)
            else:
                headers = [f"col_{i}" for i in range(len(next(reader)))]
                f.seek(0)
            
            batch = []
            for row in reader:
                record = {headers[i]: row[i] for i in range(len(headers))}
                
                if transform:
                    record = transform(record)
                
                batch.append(record)
                if len(batch) >= batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch

    def to_dataframe(self, chunksize: int = 10000):
        try:
            import pandas as pd
            return pd.read_csv(
                self.filepath,
                delimiter=self.delimiter,
                quotechar=self.quotechar,
                chunksize=chunksize,
                encoding=self.detected_encoding
            )
        except ImportError:
            raise Exception("Pandas not installed. Install with 'pip install pandas'")