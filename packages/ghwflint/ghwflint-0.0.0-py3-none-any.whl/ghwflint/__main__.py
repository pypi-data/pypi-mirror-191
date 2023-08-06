#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys


def usage():
    print("  ghwflint -- https://github.com/release-engineers/y")
    print()
    print("Usage: ghwflint [-- <args>]")
    print("  -- <args>          GitHub Workflow to validate")


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        usage()
        exit(0)

    workflows = []
    while len(args) > 0:
        arg = args.pop(0)
        if arg == '-h' or arg == '--help':
            usage()
            exit(0)
        elif arg == '--':
            workflows.extend(args)
            args.clear()
        else:
            workflows.append(arg)

    pass


if __name__ == '__main__':
    main()
