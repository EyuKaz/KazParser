import pytest
from kazparser.core import KazParser

def test_auto_delimiter_detection(tmp_path):
    test_file = tmp_path / "test.tsv"
    test_file.write_text("id\tname\n1\tAlice\n2\tBob")
    
    parser = KazParser(str(test_file), delimiter='auto')
    batches = list(parser.stream())
    assert batches[0][0]['name'] == 'Alice'

def test_encoding_detection(tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_bytes("id,name\n1,Älice".encode('latin-1'))
    
    parser = KazParser(str(test_file))
    assert parser.detected_encoding == 'ISO-8859-1'