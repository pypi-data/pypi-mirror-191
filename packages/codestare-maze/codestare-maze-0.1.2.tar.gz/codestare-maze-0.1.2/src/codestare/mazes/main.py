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
    parser = argparse.ArgumentParser(prog='maze-gen')
    parser.add_argument(
        "--file",
        default='',
        help='file to redirect output'
    )
    subparsers = parser.add_subparsers(help='uses the growing tree algorithm to generate the maze')
    parser_growing_tree = subparsers.add_parser('growing_tree')
    parser_growing_tree.add_argument('w', type=int, help='Width of maze')
    parser_growing_tree.add_argument('h', type=int, help='Height of maze')
    parser_growing_tree.add_argument(
        '--choice',
        type=str,
        default='mixed',
        help='which method to choose next cell',
        choices=['random', 'last', 'mixed']
    )
    parser_growing_tree.add_argument(
        '--t',
        type=float,
        default=0,
        help="Mixes between 'random' and 'last' choice. No effect for 'choice' other than 'mixed'"
    )
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
