#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from .collection import Collection


def run():
    parser = argparse.ArgumentParser(
        prog="sc", description="manage a software collection"
    )
    subparsers = parser.add_subparsers(dest="command")
    list_parser = subparsers.add_parser("list", help="list installed repos")
    add_parser = subparsers.add_parser("add", help="add a repo")
    add_parser.add_argument("names", nargs="+")
    add_parser = subparsers.add_parser("remove", help="remove a repo")
    add_parser.add_argument("names", nargs="+")
    status_parser = subparsers.add_parser("status", help="print repo information")
    add_parser.add_argument("name", action="store")

    args = parser.parse_args()

    if args.command == "add":
        for url in args.names:
            Collection.add(url)
    elif args.command == "remove":
        for name in args.names:
            Collection.remove(name)
    elif args.command == "list":
        for r in Collection().repos:
            print(r.name)
    elif args.command == "status":
        r = Collection.find(args.names[0])
        print(" ".join([r.name, r.commit]))
