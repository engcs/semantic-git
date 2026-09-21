#!/usr/bin/env python3
"""Internal structure validator module. Use semantic_git.py as the public CLI."""
from _internal.validate_structure import *  # noqa: F401,F403

if __name__ == "__main__":
    raise SystemExit("Unsupported direct CLI. Use: python _scripts/semantic_git.py validate")
