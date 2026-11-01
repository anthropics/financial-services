#!/usr/bin/env python3
"""Harness-side schema validation for managed-agent worker output.

Usage:
    validate.py <output.json> <schema.json|schema.yaml> [--verbose]

Features:
- Supports JSON and YAML schema files
- Colored terminal output
- Verbose validation success mode
- Better error reporting with exact schema path
- File existence checking
- Graceful YAML dependency handling

Exit Codes:
    0 -> Valid
    1 -> Invalid
    2 -> Incorrect usage or runtime error
"""

import json
import sys
from pathlib import Path

import jsonschema


class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"


def load_file(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    text = path.read_text(encoding="utf-8")

    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml
        except ImportError as exc:
            raise ImportError(
                "PyYAML is required for YAML schema support.\n"
                "Install it using: pip install pyyaml"
            ) from exc

        return yaml.safe_load(text)

    return json.loads(text)


def format_validation_error(error: jsonschema.ValidationError) -> str:
    instance_path = "/".join(str(p) for p in error.absolute_path) or "root"
    schema_path = "/".join(str(p) for p in error.absolute_schema_path)

    return (
        f"{Colors.RED}INVALID{Colors.RESET}\n"
        f"Message      : {error.message}\n"
        f"Instance Path: {instance_path}\n"
        f"Schema Path  : {schema_path}"
    )


def validate(instance_data, schema_data):
    validator = jsonschema.Draft202012Validator(schema_data)
    errors = sorted(validator.iter_errors(instance_data), key=lambda e: e.path)

    if errors:
        for error in errors:
            print(format_validation_error(error), file=sys.stderr)
        return False

    return True


def print_usage():
    print(
        "Usage:\n"
        "    validate.py <output.json> <schema.json|schema.yaml> [--verbose]",
        file=sys.stderr,
    )


def main() -> int:
    if len(sys.argv) not in {3, 4}:
        print_usage()
        return 2

    verbose = "--verbose" in sys.argv

    try:
        instance_path = Path(sys.argv[1])
        schema_path = Path(sys.argv[2])

        instance = load_file(instance_path)
        schema = load_file(schema_path)

        is_valid = validate(instance, schema)

        if not is_valid:
            return 1

        if verbose:
            print(f"{Colors.GREEN}VALID{Colors.RESET}: Schema validation passed")

        return 0

    except json.JSONDecodeError as error:
        print(
            f"{Colors.RED}JSON ERROR{Colors.RESET}: {error}",
            file=sys.stderr,
        )

    except FileNotFoundError as error:
        print(
            f"{Colors.YELLOW}FILE ERROR{Colors.RESET}: {error}",
            file=sys.stderr,
        )

    except ImportError as error:
        print(
            f"{Colors.YELLOW}DEPENDENCY ERROR{Colors.RESET}: {error}",
            file=sys.stderr,
        )

    except Exception as error:
        print(
            f"{Colors.RED}UNEXPECTED ERROR{Colors.RESET}: {error}",
            file=sys.stderr,
        )

    return 2


if __name__ == "__main__":
    raise SystemExit(main())    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
