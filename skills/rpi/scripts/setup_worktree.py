#!/usr/bin/env python3
"""Create the worktrees of an rpi task from .rpi/workspace.json and .rpi/workspace.local.json.

Usage: setup_worktree.py TASKSLUG [REPO_ROOT]

REPO_ROOT defaults to the repository containing the current directory, and must hold
.rpi/workspace.json from `/rpi configure-workspaces`. Prints one `worktree: <path>` line
per repo, then `start: <path>` for the next session.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SHARED_CONFIG = ".rpi/workspace.json"
LOCAL_CONFIG = ".rpi/workspace.local.json"
TASKS_DIR = ".rpi/tasks"
REQUIRED_KEYS = ("pathTemplate", "branchTemplate", "sourceRef", "repos")


def exit_not_configured(problem: str, slug: str) -> None:
    sys.exit(
        f"failed: {problem}, so the workspace has not been set up.\n"
        "Do not create or edit the workspace config yourself. Tell the user to run "
        f"`/rpi configure-workspaces` first, then come back with `/rpi setup-worktree {slug}`."
    )


def run_git(*args: str, cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, check=True, stdout=subprocess.PIPE, text=True
    )
    return result.stdout.strip()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def merge_unique(*lists) -> list:
    return list(dict.fromkeys(item for items in lists for item in items or []))


def merge_repos(shared_repos: list, local_repos: list) -> list:
    repos = {repo["localPath"]: dict(repo) for repo in shared_repos}

    for entry in local_repos:
        path = entry["localPath"]
        overrides = {k: v for k, v in entry.items() if k not in ("$patch", "copyGlobs")}

        if entry.get("$patch") == "delete":
            repos.pop(path, None)
        elif path in repos:
            copy_globs = merge_unique(repos[path].get("copyGlobs"), entry.get("copyGlobs"))
            repos[path] = {**repos[path], **overrides, "copyGlobs": copy_globs}
        else:
            repos[path] = {**overrides, "copyGlobs": entry.get("copyGlobs", [])}

    return list(repos.values())


def load_config(root: Path, slug: str) -> dict:
    shared_path = root / SHARED_CONFIG
    if not shared_path.exists():
        exit_not_configured(f"{shared_path} does not exist", slug)

    shared = read_json(shared_path)
    local = read_json(root / LOCAL_CONFIG)
    config = {**shared, **local}

    missing_keys = [key for key in REQUIRED_KEYS if key not in config]
    if missing_keys:
        exit_not_configured(
            f"the workspace config in {root}/.rpi lacks {', '.join(missing_keys)}", slug
        )

    copy_globs = merge_unique(shared.get("copyGlobs"), local.get("copyGlobs"))
    repos = merge_repos(shared.get("repos", []), local.get("repos", []))
    config["repos"] = [
        {
            "localPath": repo["localPath"],
            "sourceRef": repo.get("sourceRef", config["sourceRef"]),
            "setupCommand": repo.get("setupCommand", config.get("setupCommand", "")),
            "copyGlobs": merge_unique(copy_globs, repo.get("copyGlobs")),
        }
        for repo in repos
    ]
    return config


def render_template(template: str, slug: str, repo_name: str) -> str:
    template = re.sub(r"\{\{\s*TASKSLUG\s*\}\}", slug, template)
    return re.sub(r"\{\{\s*REPOBASENAME\s*\}\}", repo_name, template)


def copy_matching_files(repo: Path, worktree: Path, patterns: list) -> None:
    for pattern in patterns:
        for source in repo.glob(pattern):
            target = worktree / source.relative_to(repo)
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target, symlinks=True, dirs_exist_ok=True)
            else:
                shutil.copy2(source, target, follow_symlinks=False)


def exclude_from_git(worktree: Path, pattern: str) -> None:
    git_common_dir = run_git(
        "rev-parse", "--path-format=absolute", "--git-common-dir", cwd=worktree
    )
    exclude_file = Path(git_common_dir) / "info/exclude"
    exclude_file.parent.mkdir(parents=True, exist_ok=True)
    with exclude_file.open("a") as file:
        file.write(f"{pattern}\n")


def link_tasks_dir(root: Path, worktree: Path) -> None:
    tasks_dir = root / TASKS_DIR
    tasks_dir.mkdir(parents=True, exist_ok=True)
    link = worktree / TASKS_DIR
    link.parent.mkdir(parents=True, exist_ok=True)

    link_missing = not link.exists() and not link.is_symlink()
    if link_missing:
        # Relative, so the link resolves wherever the repository is mounted, e.g. inside a sandbox.
        link.symlink_to(os.path.relpath(tasks_dir, link.parent))

    check_ignore = subprocess.run(["git", "check-ignore", "-q", TASKS_DIR], cwd=worktree)
    if check_ignore.returncode != 0:
        # No trailing slash: git does not treat a symlink as a directory.
        exclude_from_git(worktree, f"/{TASKS_DIR}")


def create_worktree(root: Path, repo: Path, worktree: Path, branch: str, source_ref: str) -> None:
    run_git("-C", str(repo), "worktree", "add", "-b", branch, str(worktree), source_ref, cwd=root)


def main() -> None:
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)

    slug = sys.argv[1]
    start_dir = Path(sys.argv[2]) if len(sys.argv) == 3 else Path(".")
    root = Path(run_git("rev-parse", "--show-toplevel", cwd=start_dir))
    config = load_config(root, slug)
    branch = render_template(config["branchTemplate"], slug, "")
    start = None

    for repo_config in config["repos"]:
        repo = (root / repo_config["localPath"]).resolve()
        worktree_path = render_template(config["pathTemplate"], slug, repo.name)
        worktree = (root / Path(worktree_path).expanduser()).resolve()

        create_worktree(root, repo, worktree, branch, repo_config["sourceRef"])
        copy_matching_files(repo, worktree, repo_config["copyGlobs"])

        if repo == root:
            link_tasks_dir(root, worktree)
            start = worktree

        setup_command = repo_config["setupCommand"]
        if setup_command:
            subprocess.run(setup_command, shell=True, cwd=worktree, check=True)

        print(f"worktree: {worktree}")

    print(f"start: {start or worktree}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        command = " ".join(map(str, error.cmd)) if isinstance(error.cmd, list) else error.cmd
        sys.exit(f"failed: {command}")
