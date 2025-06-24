import json
import os


def load_schema(schema_file: str = None, schema_str: str = None) -> dict:

    if schema_file:
        if not os.path.exists(schema_file):
            raise FileNotFoundError(f"Schema file '{schema_file}' not found.")
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    elif schema_str:
        schema = json.loads(schema_str)
    else:
        raise ValueError("Either --schema-file or --schema must be provided.")

    if not isinstance(schema, dict):
        raise ValueError("Parsed schema is not a JSON object.")

    return schema
