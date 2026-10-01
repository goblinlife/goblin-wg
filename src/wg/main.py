"""Top-level CLI entry point for 'wg' command."""

import argparse
import json
import logging
import sys
from pathlib import Path

from .core.stubgen import (
    ensure_type_stubs,
    fetch_remote_spec,
    generate_type_stubs,
    get_bundled_spec_path,
    get_default_storage_path,
    get_default_stub_path,
)

logger = logging.getLogger("wg")

TITLES = {
    "wows": {"api_domain": "api.worldofwarships.com", "name": "World of Warships"},
    "wot": {"api_domain": "api.worldoftanks.com", "name": "World of Tanks"},
}


def _cmd_title_generate_stubs(args: argparse.Namespace) -> int:
    """Handle type stub generation for a specific title."""
    title = args.title
    out = args.output or get_default_stub_path(title)
    if args.force or not out.exists():
        print(f"Generating {title} type stubs to {out}...")
        generate_type_stubs(
            stub_path=out,
            storage_path=args.storage_path,
            application_id=getattr(args, "application_id", None),
            log=logger,
            api_domain=TITLES[title]["api_domain"],
            game_title=title,
        )
        print(f"Successfully generated {title} type stubs at: {out}")
    else:
        print(f"{title} type stubs already exist at {out}. Use --force to regenerate.")
    return 0


def _cmd_title_fetch_spec(args: argparse.Namespace) -> int:
    """Handle spec download for a specific title."""
    title = args.title
    target_storage = args.storage_path or get_default_storage_path(title)
    spec_path = target_storage / f"{title}_api_spec.json"
    print(f"Fetching {title} API spec to {spec_path}...")
    data = fetch_remote_spec(
        spec_path=spec_path, log=logger, api_domain=TITLES[title]["api_domain"], game_title=title
    )
    if data:
        meta = data.get("_meta", {})
        print(f"{title} spec updated successfully. Version: {meta.get('api_version', 'Unknown')}")
        if args.generate_stubs:
            print("Regenerating stubs from newly fetched spec...")
            generate_type_stubs(
                spec_data=data,
                storage_path=target_storage,
                application_id=getattr(args, "application_id", None),
                log=logger,
                api_domain=TITLES[title]["api_domain"],
                game_title=title,
            )
            print("Stubs regenerated.")
        return 0
    print("Spec was not modified or fetch failed.")
    return 1


def _cmd_title_info(args: argparse.Namespace) -> int:
    """Display information about spec and stubs for a specific title."""
    title = args.title
    storage_dir = args.storage_path or get_default_storage_path(title)
    spec_path = storage_dir / f"{title}_api_spec.json"
    stub_path = get_default_stub_path(title)
    bundled_path = get_bundled_spec_path(title)

    print(f"=== goblin-wg ({TITLES[title]['name']}) ===")
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


def _build_title_subparser(subparsers: argparse._SubParsersAction, title: str) -> None:
    """Configure subcommand tree for a specific game title."""
    title_info = TITLES[title]
    title_parser = subparsers.add_parser(
        title,
        help=f"{title_info['name']} API operations",
    )
    title_parser.add_argument(
        "--storage-path",
        "-s",
        type=Path,
        default=None,
        help="Custom storage directory for cached API spec",
    )
    title_parser.add_argument(
        "--application-id",
        "-a",
        type=str,
        default=None,
        help="Wargaming application_id for fetching game metadata",
    )

    title_subparsers = title_parser.add_subparsers(
        dest="title_command",
        help=f"{title.upper()} action to execute",
    )

    stubgen_parser = title_subparsers.add_parser(
        "generate-stubs",
        aliases=["stubgen"],
        help=f"Generate or regenerate {title} type stubs",
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

    fetch_parser = title_subparsers.add_parser(
        "fetch-spec",
        help=f"Download latest {title_info['name']} API spec",
    )
    fetch_parser.add_argument(
        "--generate-stubs",
        "-g",
        action="store_true",
        help="Regenerate stubs after fetching",
    )

    title_subparsers.add_parser("info", help=f"Show {title.upper()} configuration and spec info")


def _build_compliance_subparser(subparsers: argparse._SubParsersAction) -> None:
    """Configure 'compliance' subcommand tree."""
    compliance_parser = subparsers.add_parser(
        "compliance",
        help="GDPR and data compliance utilities",
    )
    compliance_subparsers = compliance_parser.add_subparsers(
        dest="compliance_command",
        help="Compliance action to execute",
    )

    extract_parser = compliance_subparsers.add_parser(
        "extract-deleted",
        help="Extract account IDs from WG's deleted_accounts.zip",
    )
    extract_parser.add_argument(
        "file",
        type=Path,
        help="Path to deleted_accounts.zip or accounts.csv",
    )
    extract_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "csv", "text"],
        default="json",
        help="Output format (default: json)",
    )


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
    for title in TITLES:
        _build_title_subparser(subparsers, title)
    _build_compliance_subparser(subparsers)
    return parser


def _dispatch_compliance(args: argparse.Namespace) -> int:
    """Dispatch commands for 'compliance' title."""
    from .compliance import extract_deleted_account_ids

    if args.compliance_command == "extract-deleted":
        try:
            ids = list(extract_deleted_account_ids(args.file))
            if args.format == "json":
                import json

                print(json.dumps(ids))
            elif args.format == "csv":
                print("account_id")
                for acc_id in ids:
                    print(acc_id)
            elif args.format == "text":
                for acc_id in ids:
                    print(acc_id)
            return 0
        except Exception as e:
            logger.error(f"Failed to extract deleted accounts: {e}")
            return 1

    print("Please specify a compliance action (e.g. extract-deleted). Use --help for details.")
    return 0


def _dispatch_title(args: argparse.Namespace) -> int:
    """Dispatch commands for a specific title."""
    if args.title_command in ("generate-stubs", "stubgen"):
        return _cmd_title_generate_stubs(args)
    if args.title_command == "fetch-spec":
        return _cmd_title_fetch_spec(args)
    if args.title_command == "info":
        return _cmd_title_info(args)

    title = args.title
    stub_path = get_default_stub_path(title)
    if not stub_path.exists():
        print(f"Initial setup: {title} type stubs not found. Autorunning type stub generation...")
        ensure_type_stubs(
            storage_path=args.storage_path,
            log=logger,
            api_domain=TITLES[title]["api_domain"],
            game_title=title,
        )
        print(f"{title} type stubs generated at: {stub_path}")
        return 0

    print(
        f"Please specify a {title} action (generate-stubs, fetch-spec, info). Use --help for details."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI main entry point for 'wg'."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")

    if args.title in TITLES:
        return _dispatch_title(args)

    if args.title == "compliance":
        return _dispatch_compliance(args)

    # If invoked as bare 'wg' with no arguments, we can default to wows
    stub_path = get_default_stub_path("wows")
    if not stub_path.exists():
        print("Initial setup: WoWS type stubs not found. Autorunning type stub generation...")
        ensure_type_stubs(log=logger, api_domain=TITLES["wows"]["api_domain"], game_title="wows")
        print(f"WoWS type stubs generated at: {stub_path}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
