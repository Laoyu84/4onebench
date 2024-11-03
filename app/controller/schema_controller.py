import os
import yaml
from pathlib import Path
from models.tables import TableSchema

class SchemaController:
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent / 'config' / 'tables'

    def read_yaml_schema(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return TableSchema(data['table'], data['columns'])

    def load_all_schemas(self):
        schemas = []
        for yaml_file in self.config_dir.glob('*.yaml'):
            schemas.append(self.read_yaml_schema(yaml_file))
        return schemas