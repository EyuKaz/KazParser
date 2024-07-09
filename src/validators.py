from jsonschema import validate, ValidationError
from typing import List, Dict

class SchemaValidator:
    def __init__(self, schema: Dict):
        self.schema = schema

    def validate_stream(self, stream: Generator) -> Generator:
        errors = []
        for batch in stream:
            validated_batch = []
            for record in batch:
                try:
                    validate(instance=record, schema=self.schema)
                    validated_batch.append(record)
                except ValidationError as e:
                    errors.append({
                        'record': record,
                        'error': str(e)
                    })
            yield validated_batch
        if errors:
            print(f"Validation completed with {len(errors)} errors")
            # Optionally write errors to file