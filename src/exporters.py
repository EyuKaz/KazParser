from typing import List, Dict

class SQLExporter:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def export(self, data: List[Dict]) -> str:
        """Generate SQL INSERT statements from data"""
        if not data:
            return ""
            
        columns = data[0].keys()
        values = []
        for row in data:
            formatted = []
            for v in row.values():
                if isinstance(v, str):
                    formatted.append(f"'{v}'")
                else:
                    formatted.append(str(v))
            values.append(f"({', '.join(formatted)})")
        
        return f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES\n" + \
               ",\n".join(values) + ";"