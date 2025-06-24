import argparse
import json
import sys
from utils.schema_loader import load_schema
from generators.base import generate_value


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate structured JSON data from a user-defined schema."
    )

    # Provide --schema-file or --schema (One must be provided)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f", "--schema-file",
        dest="schema_file",
        help="Path to JSON schema file"
    )
    group.add_argument(
        "-s", "--schema",
        dest="schema_str",
        help="Inline JSON schema string"
    )

    parser.add_argument(
        "-c", "--count",
        type=int,
        required=True,
        help="Number of records to generate"
    )
    parser.add_argument(
        "-o", "--output",
        dest="output",
        help="Output file path. Omit to print to console"
    )

    return parser.parse_args()


def generate_data(schema_dict: dict, count: int) -> list[dict]:
    records = []
    for _ in range(count):
        record = {}
        for field, spec in schema_dict.items():
            try:
                record[field] = generate_value(spec)
            except ValueError as e:
                print(f"Error generating field '{field}': {e}", file=sys.stderr)
                sys.exit(1)
        records.append(record)
    return records


def main():
    args = parse_args()

    # Load the JSON schema (file or inline)
    try:
        schema_dict = load_schema(
            schema_file=args.schema_file,
            schema_str=args.schema_str
        )
    except Exception as e:
        print(f"Schema loading error: {e}", file=sys.stderr)
        sys.exit(1)

    src = args.schema_file or "<inline schema>"
    print(f"Schema loaded      : {src}")
    print(f"Generating {args.count} record(s)")

    # Generate the data
    data = generate_data(schema_dict, args.count)

    # Serialize to JSON
    output_json = json.dumps(data, indent=2)

    # Write to file or stdout
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_json)
        except Exception as e:
            print(f"Failed to write output to file: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"Successfully wrote {len(data)} records to {args.output}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()