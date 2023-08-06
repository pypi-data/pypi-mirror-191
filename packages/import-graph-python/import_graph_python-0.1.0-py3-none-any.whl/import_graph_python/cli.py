"""CLI interface for import-graph-python."""
import argparse

import import_graph_python


class CLIArgs(argparse.Namespace):
    """Type hints for the CLI arguments."""

    repo_root: str
    filepath: str


def cli() -> None:
    """Runs the CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root")
    parser.add_argument("filepath")

    args = parser.parse_args(namespace=CLIArgs())

    deps = import_graph_python.get_file_dependencies(args.repo_root, args.filepath)

    for dep in deps:
        print(dep)


if __name__ == "__main__":
    cli()
