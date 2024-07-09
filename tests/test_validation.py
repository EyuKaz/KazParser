import pytest
import orjson
from kazparser.validators import SchemaValidator
from kazparser.core import KazParser

@pytest.fixture
def sample_schema():
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string", "minLength": 3},
            "email": {"format": "email"},
            "isActive": {"type": "boolean"}
        },
        "required": ["id", "name"]
    }

@pytest.fixture
def valid_data():
    return [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "isActive": True},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ]

@pytest.fixture
def invalid_data():
    return [
        {"id": "three", "name": "Al"},  # Invalid id type and short name
        {"name": "Charlie", "email": "invalid-email"},  # Missing id
        {"id": 4, "name": "Dave", "isActive": "yes"}  # Invalid boolean
    ]

def test_valid_data(sample_schema, valid_data):
    validator = SchemaValidator(sample_schema)
    validated = list(validator.validate_stream([valid_data]))
    assert len(validated[0]) == 2
    assert "Validation complete: 0" in validator.validation_report()

def test_invalid_data(sample_schema, invalid_data):
    validator = SchemaValidator(sample_schema)
    validated = list(validator.validate_stream([invalid_data]))
    assert len(validated[0]) == 0  # All invalid records are filtered
    assert "Validation complete: 3" in validator.validation_report()

def test_mixed_data(sample_schema):
    mixed_data = [
        {"id": 5, "name": "Eve", "email": "eve@example.com"},
        {"id": "six", "name": "Frank"},  # Invalid id
        {"name": "Grace", "email": "grace@example.com"}  # Missing id
    ]
    
    validator = SchemaValidator(sample_schema)
    validated_batches = list(validator.validate_stream([mixed_data]))
    
    assert len(validated_batches[0]) == 1  # Only first record is valid
    assert "Validation complete: 2" in validator.validation_report()

def test_real_file_validation(tmp_path):
    # Create temporary test file
    test_file = tmp_path / "test.csv"
    test_file.write_text("id,name,email\n1,Alice,alice@example.com\n2,Bob,invalid-email")

    # Create schema file
    schema_file = tmp_path / "schema.json"
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"format": "email"}
        },
        "required": ["id", "name"]
    }
    schema_file.write_text(orjson.dumps(schema).decode())

    # Validate through CLI
    parser = KazParser(str(test_file))
    validator = SchemaValidator(schema)
    
    validated = list(validator.validate_stream(parser.stream()))
    assert len(validated[0]) == 1  # Second record has invalid email