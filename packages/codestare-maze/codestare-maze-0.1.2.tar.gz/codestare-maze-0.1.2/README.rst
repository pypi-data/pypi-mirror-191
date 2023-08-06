codestar-maze
=============

Simple maze generators in python.

Usage
-----
Installing the package also installs the `maze-gen` entry point.

::

    usage: maze-gen [-h] [--file FILE] {growing_tree} ...

    positional arguments:
      {growing_tree}  uses the growing tree algorithm to generate the maze

    options:
      -h, --help      show this help message and exit
      --file FILE     file to redirect output

Currently only the `growing_tree` algorithm is supported. The appropriate
subcommand takes the following arguments:

::

    usage: maze-gen growing_tree [-h] [--choice {random,last,mixed}] [--t T] w h

    positional arguments:
      w                     Width of maze
      h                     Height of maze

    options:
      -h, --help            show this help message and exit
      --choice {random,last,mixed}
                            which method to choose next cell
      --t T                 Mixes between 'random' and 'last' choice. No effect for 'choice' other than 'mixed'
