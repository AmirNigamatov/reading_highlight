import argparse

from highlights import add_highlight, search_highlights, view_highlights


def main():
    parser = argparse.ArgumentParser(description="Reading Highlights")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    add_parser = subparsers.add_parser("add", help="Add a new highlight")
    add_parser.add_argument("--text", required=True, help="Text of the highlight")
    add_parser.add_argument("--source", required=True, help="Source (e.g., book title)")
    add_parser.add_argument("--tags", required=True, help="Tags separated by commas")

    subparsers.add_parser("view", help="View all highlights")

    search_parser = subparsers.add_parser("search", help="Search highlights")
    search_parser.add_argument("--query", required=True, help="Search query")

    args = parser.parse_args()

    if args.command == "add":
        highlight = add_highlight(args.text, args.source, args.tags)
        print(f"Added: {highlight.text[:50]}... from {highlight.source}")

    elif args.command == "view":
        highlights = view_highlights()
        if not highlights:
            print("No highlights yet.")
        for i, h in enumerate(highlights, 1):
            print(f"{i}. \"{h.text}\" - {h.source} (Tags: {', '.join(h.tags)})")

    elif args.command == "search":
        results = search_highlights(args.query)
        if not results:
            print("No matches found.")
        for i, h in enumerate(results, 1):
            print(f"{i}. \"{h.text}\" - {h.source} (Tags: {', '.join(h.tags)})")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
