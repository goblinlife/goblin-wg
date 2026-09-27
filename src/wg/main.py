"""Top-level CLI entry point for 'wg' command."""

import argparse
import json
import logging
import sys
from pathlib import Path

from .wows._stubgen import (
    ensure_type_stubs,
    fetch_remote_spec,
    generate_type_stubs,
    get_bundled_spec_path,
    get_default_storage_path,
    get_default_stub_path,
)

logger = logging.getLogger("wg")


def _cmd_wows_generate_stubs(args: argparse.Namespace) -> int:
    """Handle World of Warships stub generation."""
    out = args.output or get_default_stub_path()
    if args.force or not out.exists():
        print(f"Generating WoWS type stubs to {out}...")
        generate_type_stubs(
            stub_path=out,
            storage_path=args.storage_path,
            application_id=getattr(args, "application_id", None),
            log=logger,
        )
        print(f"Successfully generated WoWS type stubs at: {out}")
    else:
        print(f"WoWS type stubs already exist at {out}. Use --force to regenerate.")
    return 0


def _cmd_wows_fetch_spec(args: argparse.Namespace) -> int:
    """Handle World of Warships spec download."""
    target_storage = args.storage_path or get_default_storage_path()
    spec_path = target_storage / "wows_api_spec.json"
    print(f"Fetching WoWS API spec to {spec_path}...")
    data = fetch_remote_spec(spec_path=spec_path, log=logger)
    if data:
        meta = data.get("_meta", {})
        print(f"WoWS spec updated successfully. Version: {meta.get('api_version', 'Unknown')}")
        if args.generate_stubs:
            print("Regenerating stubs from newly fetched spec...")
            generate_type_stubs(
                spec_data=data,
                storage_path=target_storage,
                application_id=getattr(args, "application_id", None),
                log=logger,
            )
            print("Stubs regenerated.")
        return 0
    print("Spec was not modified or fetch failed.")
    return 1


def _cmd_wows_info(args: argparse.Namespace) -> int:
    """Display information about WoWS spec and stubs."""
    storage_dir = args.storage_path or get_default_storage_path()
    spec_path = storage_dir / "wows_api_spec.json"
    stub_path = get_default_stub_path()
    bundled_path = get_bundled_spec_path()

    print("=== goblin-wg (World of Warships) ===")
    print(f"Storage path:          {storage_dir}")
    print(f"Spec file path:        {spec_path} (exists: {spec_path.exists()})")
    print(f"Bundled spec fallback: {bundled_path} (exists: {bundled_path.exists()})")
    print(f"Type stubs path:       {stub_path} (exists: {stub_path.exists()})")

    if spec_path.exists():
        try:
            data = json.loads(spec_path.read_text(encoding="utf-8"))
            meta = data.get("_meta", {})
            methods_count = len(data.get("methods", []))
            print(f"API Version:           {meta.get('api_version', 'Unknown')}")
            print(f"Spec Fetch Date:       {meta.get('date', 'Unknown')}")
            print(f"Available Endpoints:   {methods_count}")
        except Exception as err:
            print(f"Error reading spec:    {err}")
    return 0


def _build_wows_subparser(subparsers: argparse._SubParsersAction) -> None:
    """Configure 'wows' subcommand tree."""
    wows_parser = subparsers.add_parser(
        "wows",
        help="World of Warships API operations",
    )
    wows_parser.add_argument(
        "--storage-path",
        "-s",
        type=Path,
        default=None,
        help="Custom storage directory for cached API spec",
    )
    wows_parser.add_argument(
        "--application-id",
        "-a",
        type=str,
        default=None,
        help="Wargaming application_id for fetching game metadata",
    )

    wows_subparsers = wows_parser.add_subparsers(
        dest="wows_command",
        help="WoWS action to execute",
    )

    stubgen_parser = wows_subparsers.add_parser(
        "generate-stubs",
        aliases=["stubgen"],
        help="Generate or regenerate client.pyi type stubs",
    )
    stubgen_parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output destination path for client.pyi",
    )
    stubgen_parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force regeneration even if stub file exists",
    )

    fetch_parser = wows_subparsers.add_parser(
        "fetch-spec",
        help="Download latest World of Warships API spec",
    )
    fetch_parser.add_argument(
        "--generate-stubs",
        "-g",
        action="store_true",
        help="Regenerate stubs after fetching",
    )

    wows_subparsers.add_parser("info", help="Show WoWS configuration and spec info")


def _build_parser() -> argparse.ArgumentParser:
    """Construct top-level 'wg' CLI parser."""
    parser = argparse.ArgumentParser(
        prog="wg",
        description="Wargaming CLI and developer toolkit.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose debug logging",
    )

    subparsers = parser.add_subparsers(dest="title", help="Game or service module")
    _build_wows_subparser(subparsers)
    return parser


def _dispatch_wows(args: argparse.Namespace) -> int:
    """Dispatch commands for 'wows' title."""
    if args.wows_command in ("generate-stubs", "stubgen"):
        return _cmd_wows_generate_stubs(args)
    if args.wows_command == "fetch-spec":
        return _cmd_wows_fetch_spec(args)
    if args.wows_command == "info":
        return _cmd_wows_info(args)

    # If 'wg wows' called without subcommands:
    stub_path = get_default_stub_path()
    if not stub_path.exists():
        print("Initial setup: WoWS type stubs not found. Autorunning type stub generation...")
        ensure_type_stubs(storage_path=args.storage_path, log=logger)
        print(f"WoWS type stubs generated at: {stub_path}")
        return 0

    print(
        "Please specify a wows action (generate-stubs, fetch-spec, info). Use --help for details."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI main entry point for 'wg'."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")

    if args.title == "wows":
        return _dispatch_wows(args)

    # If invoked as bare 'wg' with no arguments, check if stubs exist
    stub_path = get_default_stub_path()
    if not stub_path.exists():
        print("Initial setup: WoWS type stubs not found. Autorunning type stub generation...")
        ensure_type_stubs(log=logger)
        print(f"WoWS type stubs generated at: {stub_path}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
