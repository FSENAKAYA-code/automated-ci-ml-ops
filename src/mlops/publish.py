"""Explicitly gated Git branch publishing helper; never auto-commits or pushes."""

import argparse
import subprocess
from pathlib import Path


def publish_all_branches(repo: Path, remote: str, *, confirm: bool = False) -> None:
    if not confirm:
        raise ValueError("publishing requires the explicit --confirm flag")
    if not remote or remote.startswith("-"):
        raise ValueError("a valid configured remote name is required")
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    if status.strip():
        raise ValueError("refusing to publish with uncommitted changes")
    remotes = subprocess.run(
        ["git", "remote"], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.splitlines()
    if remote not in remotes:
        raise ValueError(f"Git remote {remote!r} is not configured")
    subprocess.run(["git", "push", "--all", remote], cwd=repo, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    publish_all_branches(args.repo, args.remote, confirm=args.confirm)


if __name__ == "__main__":
    main()
