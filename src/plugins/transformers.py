from datetime import datetime

class EmailNormalizer:
    def __init__(self, email_field: str = 'email'):
        self.email_field = email_field

    def __call__(self, record: dict) -> dict:
        if self.email_field in record:
            email = record[self.email_field].lower().strip()
            record[self.email_field] = email
            record['domain'] = email.split('@')[-1] if '@' in email else ''
        return record

class TimestampAdder:
    def __init__(self, timestamp_field: str = 'processed_at'):
        self.timestamp_field = timestamp_field

    def __call__(self, record: dict) -> dict:
        record[self.timestamp_field] = datetime.utcnow().isoformat()
        return record