#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from ghwflint.validator import Validator


def usage():
    print("  ghwflint -- https://github.com/release-engineers/lint-github-workflow")
    print()
    print("Usage: ghwflint [-- <args>]")
    print("  -- <args>          GitHub Workflows to be validated")


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

    validator = Validator()
    for workflow in workflows:
        print(f"\t{workflow}")
        validator.validate(workflow)


if __name__ == '__main__':
    main()
