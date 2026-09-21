#!/usr/bin/env python3
"""Internal compiled-context module. Use semantic_git.py as the public CLI."""
from _internal.compile_semantic_context import *  # noqa: F401,F403

if __name__ == "__main__":
    raise SystemExit("Unsupported direct CLI. Use: python _scripts/semantic_git.py compiled ...")
