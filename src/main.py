import argparse
import os
import sys

sys.path.append(os.path.dirname(__file__))

from highlights import add_highlight, load_highlights


def main():
    parser = argparse.ArgumentParser(description="Reading Highlights MVP")
    parser.add_argument("command", choices=["add", "list"], help="Command to execute")
    parser.add_argument("--text", help="Text of the highlight")
    parser.add_argument("--source", help="Source of the highlight")
    parser.add_argument("--tags", nargs="*", help="Tags for the highlight")

    args = parser.parse_args()

    if args.command == "add":
        if not args.text or not args.source:
            print("Error: --text and --source are required for add command")
            return
        add_highlight(args.text, args.source, args.tags or [])
        print("Highlight added successfully")
    elif args.command == "list":
        highlights = load_highlights()
        for h in highlights:
            print(f"Text: {h.text}")
            print(f"Source: {h.source}")
            print(f"Tags: {', '.join(h.tags)}")
            print("---")


if __name__ == "__main__":
    main()
