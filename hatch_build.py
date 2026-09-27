"""Hatchling custom build hook to autorun type stub generation during package build."""

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    class BuildHookInterface:
        root: str
else:
    try:
        from hatchling.builders.hooks.plugin.interface import BuildHookInterface
    except ImportError:
        class BuildHookInterface:
            root: str


class CustomBuildHook(BuildHookInterface):
    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        """Run type stub generation before wheel / sdist artifacts are assembled."""
        # Ensure package src directory is on sys.path
        src_path = Path(self.root) / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from wg.wows._stubgen import generate_type_stubs

            target_stub = Path(self.root) / "src" / "wg" / "wows" / "client.pyi"
            generate_type_stubs(stub_path=target_stub)
        except Exception as exc:
            # Do not fail build if network is unavailable; check if stub already exists
            target_stub = Path(self.root) / "src" / "wg" / "wows" / "client.pyi"
            if not target_stub.exists():
                print(
                    f"Warning: Failed to generate type stubs during build: {exc}", file=sys.stderr
                )
