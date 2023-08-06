"""
CLI for maze generator
"""
import argparse
import contextlib
import pathlib
import sys
import uuid
from typing import ContextManager

from codestare.mazes.algorithms import growing_tree


def parse_args() -> argparse.Namespace:
    """
    Returns: namespace of arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        default=''
    )
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_growing_tree = subparsers.add_parser('growing_tree')
    parser_growing_tree.add_argument('w', type=int)
    parser_growing_tree.add_argument('h', type=int)
    parser_growing_tree.add_argument('--choice', type=str, default='default_choice')
    parser_growing_tree.set_defaults(func=growing_tree)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def out(file) -> ContextManager:
    """maybe redirect to file"""

    @contextlib.contextmanager
    def ctx():
        yield sys.stdout

    if not file:
        return ctx()
    else:
        file = pathlib.Path(file)
        if file.exists():
            file = file.parent / f"{file.stem}_{uuid.uuid4()}{file.suffix}"

        return open(file, 'w', encoding='utf-8')


def main():
    """CLI entry point"""
    args = parse_args()
    with out(args.file) as sys.stdout:
        args.func(args)


if __name__ == '__main__':
    main()
