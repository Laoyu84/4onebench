import yaml

class Column:
    def __init__(self, name, desc=None):
        self.name = name
        self.desc = desc
    def __str__(self):
        if self.desc:
            return f"'{self.name}'{self.desc}"
        return f"'{self.name}'"

class TableSchema:
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = [Column(col['name'], col.get('desc')) for col in columns]

    def __str__(self):
        column_names = [col.name for col in self.columns]
        base_string = f"{self.table_name}包含属性:{', '.join(repr(name) for name in column_names)};"
        
        additional_info = [str(col) for col in self.columns if col.desc]
        
        if additional_info:
            base_string += '\n-' + ';\n-'.join(additional_info) + ';'

        return base_string