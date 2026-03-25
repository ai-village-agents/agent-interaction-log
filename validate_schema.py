#!/usr/bin/env python3
import json
import jsonschema
import sys
import os

def validate_json_against_schema(json_file, schema_file):
    """Validate a JSON file against a JSON Schema."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            instance = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        return False, f"Failed to load JSON file {json_file}: {e}"
    
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        return False, f"Failed to load schema file {schema_file}: {e}"
    
    try:
        jsonschema.validate(instance=instance, schema=schema)
        return True, f"✓ {json_file} validates against {schema_file}"
    except jsonschema.ValidationError as e:
        return False, f"✗ Validation error in {json_file}: {e.message}"
    except jsonschema.SchemaError as e:
        return False, f"✗ Schema error in {schema_file}: {e}"

def main():
    schema_path = "standards/birch-continuity-schema-v1.json"
    # Test with the canonical record
    record_path = "research/birch-phase2-cognirelay-opus-metrics/2026-03-25-claude-opus-4.5-continuity-v1.json"
    
    print("Validating canonical continuity record against schema...")
    success, message = validate_json_against_schema(record_path, schema_path)
    print(message)
    
    # Also check schema against meta-schema (optional)
    print("\nChecking schema validity (meta-schema)...")
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        # Use Draft 7 meta-schema
        jsonschema.Draft7Validator.check_schema(schema)
        print("✓ Schema is valid JSON Schema (Draft 7)")
    except Exception as e:
        print(f"✗ Schema validation error: {e}")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
