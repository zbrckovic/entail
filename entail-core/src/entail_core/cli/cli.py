import argparse
import os
from pathlib import Path
from urllib.parse import urlparse

from entail_core.parser.ast_processing import process_ast
from entail_core.parser.parsing import parse

parser = argparse.ArgumentParser()
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'))
args = parser.parse_args(
    ['../../../../entail-deductions/modus-tollens.entail'])

if args.infile is not None:
    path = Path(args.infile.name)
    extension = path.suffix

    if path.suffix != '.entail':
        raise Exception('File doesn\'t have the extension ".entail".')

    text = args.infile.read()

    parse_result = parse(text)

    if len(parse_result.errors) > 0:
        # Stop the process if there were errors.
        raise parse_result.errors[0]

    entail_file = process_ast(parse_result.tree)

    print('Deduction is valid.')
