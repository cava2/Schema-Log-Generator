import argparse
import json
import sys
from utils.schema_loader import load_schema

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


def main():
    args = parse_args()

    # Load schema from file or inline JSON
    try:
        schema = load_schema(schema_file=args.schema_file, schema_str=args.schema_str)
    except Exception as e:
        print(f" Schema loading error: {e}", file=sys.stderr)
        sys.exit(1)

    # Echo schema back to the user
    src = args.schema_file if args.schema_file else "<inline schema>"
    print(f"Schema loaded  :{src}.")
    print(f"Generating {args.count} logs.")

    # TODO: implement generate_data(schema: dict, count: int) -> list[dict]
    # data = generate_data(schema, args.count)

    # For now, stub out empty data list
    data = []

    # Output handling: file or stdout
    output_json = json.dumps(data, indent=2)
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_json)
        except Exception as e:
            print(f" Failed to write output to file: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"Successfully wrote {len(data)} records to {args.output}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
