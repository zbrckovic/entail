import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from entail_core.constants import ENTAIL_FILE_EXTENSION


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'))
    args = parser.parse_args(
        ['../../../entail-deductions/modus-tollens.entail'])

    file = extract_input_file(args)

    return CLIResult(file)


def extract_input_file(args):
    # Get absolute path to the file.
    if args.infile is None:
        return

    path = Path(args.infile.name).resolve()
    validate_file_extension(path)
    text = args.infile.read()
    return path, text


def validate_file_extension(path):
    if path.suffix != '.' + ENTAIL_FILE_EXTENSION:
        raise Exception(f'The file doesn\'t have the required extension '
                        f'"{ENTAIL_FILE_EXTENSION}".')


@dataclass
class CLIResult:
    file: Optional[tuple[Path, str]]
