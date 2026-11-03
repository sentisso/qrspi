---
name: configure-workspaces
description: Propose and generate workspace configuration files (.rpi/workspace.json and .rpi/workspace.local.json) for a repository
---

## Purpose

This skill reads the project, proposes a concise workspace configuration, writes the approved files, and validates them.

The workspace config files control how `setup-worktree` creates worktrees:
- `.rpi/workspace.json` — shared team configuration, safe to commit
- `.rpi/workspace.local.json` — machine-specific overrides, gitignored

Use plain, brief language. State each point as one human speaking to another.

## Steps to follow

<step index=0>

### Step 0: Select the repository

Check the current directory and home directory:

```bash
pwd
printf '%s\n' "$HOME"
git rev-parse --show-toplevel
```

If `git rev-parse` succeeds, use that repository root as the working directory. State the path in one short sentence.

If the current directory is the home directory and it is not inside a Git repository, ask one question:

```
Which repository should I configure? Send its path.
```

Use the same question when the current directory is not a Git repository. After the user gives a path, confirm it with `git -C <path> rev-parse --show-toplevel` and use the returned root.

</step>

<step index=1>

### Step 1: Read the project

Read any existing workspace config files: `.rpi/workspace.json` and `.rpi/workspace.local.json`.

Run all file reads and commands from the selected repository root.

Check for coordination-repo signals (Claude config, additional sibling repos). Read `.claude/settings.json`, `package.json`, `Makefile` and `README.md`, and run:

```bash
ls -la ../
git remote -v
```

Use an existing workspace config as the starting point. Infer changes from the repository and the user's request.

</step>

<step index=2>

### Step 2: Build the proposal

Infer a complete proposal from project files and common defaults.

- Use a single-repository config unless the project clearly coordinates related sibling repositories.
- For one repository, use `{ "localPath": "." }`.
- For multiple repositories, include the related paths.
- Use `.rpi/workspaces/{{ TASKSLUG }}/{{ REPOBASENAME }}` as the default path template. A relative path template resolves from the selected repository root.
- Use `origin/main` as the default source ref, or whatever default remote the user prefers (e.g. upstream/main - if there are multiple remotes, ask)
- Infer a setup command from project scripts, package manager files, the Makefile, and the README.
- Include local files that exist and are useful in a worktree, such as `.env`, `.env.local`, `.env.development.local`, `.claude/settings.local.json`, and `.rpi/workspace.local.json`.
- Put machine-specific values in `.rpi/workspace.local.json`.

The first response after project inspection must show the proposed `.rpi/workspace.json` as a fenced `json` block. If local overrides are useful, show `.rpi/workspace.local.json` in a second fenced `json` block. End with one short line:

```
Tell me what to change, or approve this config.
```

When the user gives feedback, update and print the complete proposed JSON again.

</step>

<step index=3>

### Step 3: Validate the proposal

Validate the proposed config before asking for approval.

**For single-repo projects, workspace.json looks like:**

```json
{
  "disabled": false,
  "pathTemplate": ".rpi/workspaces/{{ TASKSLUG }}/{{ REPOBASENAME }}",
  "branchTemplate": "{{ TASKSLUG }}",
  "sourceRef": "origin/main",
  "setupCommand": "",
  "copyGlobs": [
    ".env",
    ".env.local",
    ".env.development.local",
    ".claude/settings.local.json",
    ".rpi/workspace.local.json"
  ],
  "repos": [
    {
      "localPath": ".",
      "description": "Selected repository"
    }
  ]
}
```

**For multi-repo projects (coordination repos), workspace.json looks like:**

```json
{
  "disabled": false,
  "pathTemplate": ".rpi/workspaces/{{ TASKSLUG }}/{{ REPOBASENAME }}",
  "branchTemplate": "{{ TASKSLUG }}",
  "sourceRef": "origin/main",
  "setupCommand": "pnpm install",
  "copyGlobs": [
    ".env",
    ".env.local",
    ".rpi/workspace.local.json"
  ],
  "repos": [
    {
      "localPath": ".",
      "description": "Coordination repo"
    },
    {
      "localPath": "../api",
      "description": "API service",
      "setupCommand": "pnpm install"
    },
    {
      "localPath": "../web",
      "description": "Web frontend",
      "sourceRef": "origin/main"
    }
  ]
}
```

**Config rules to follow:**
- `localPath: "."` refers to the selected repository itself (the one containing this config); other entries are sibling paths relative to it
- Template variables are `{{ TASKSLUG }}` and `{{ REPOBASENAME }}` only
- `copyGlobs` is additive with de-duplication (workspace.json → workspace.local.json → per-repo), never replaced
- Repo entries may override `sourceRef`, `setupCommand`, and `copyGlobs` — `branchTemplate` is always root-level
- `$patch: "delete"` is supported only in `workspace.local.json` repos entries, not in `workspace.json`
- `disabled: true` at root level makes `setup-worktree` check out the task branch instead of creating worktrees

**Validate the generated config:**

```bash
git remote -v
```

For each repo `localPath`:
- Check the directory exists: `ls -la <localPath>`
- Check it's a git repo: `git -C <localPath> rev-parse --git-dir`
- If `sourceRef` has a remote prefix, verify the remote exists: `git -C <localPath> remote -v | grep <prefix>`

If `setupCommand` is set, state what it does in one sentence. Setup commands run after worktree creation.

</step>

<step index=4>

### Step 4: Write the approved config

After approval, write the proposed config.

Write `.rpi/workspace.json`.

If there are local overrides, write `.rpi/workspace.local.json` and ensure it is gitignored.

Read `.gitignore` and check for the `.rpi/workspace.local.json` and `.rpi/workspaces/` entries. Add each missing entry:

```bash
echo '.rpi/workspace.local.json' >> .gitignore
echo '.rpi/workspaces/' >> .gitignore
```

</step>

<step index=5>

### Step 5: Confirm and summarize

Give a short summary:

- Files written
- Number of repos configured
- Path template that will be used
- Setup command (if any)
- Copy globs summary

Explain the next steps:

```
The workspace configuration is now ready.

When you run `/rpi setup-worktree <task-slug>`, it will:
- Create a git worktree for each configured repo at the rendered path
- Copy the configured files into each worktree
- Run the setup command in each worktree
```

If the user is on a team, remind them to commit `workspace.json` (but not `workspace.local.json`):

```bash
git add .rpi/workspace.json
git status
```

</step>

## Key concepts for this skill

### Template variables

Only two template variables are supported:
- `{{ TASKSLUG }}` — the task slug (e.g. `eng-123-small-fix`)
- `{{ REPOBASENAME }}` — the basename of each repo's resolved `localPath` (e.g. `humanlayer`, `api`, `web`)

### Repo precedence rules

Effective config = defaults → workspace.json → workspace.local.json

For `repos[]`:
- Local entry with matching `localPath` merges into that repo (local fields win)
- Local entry with new `localPath` adds a new repo
- Local entry with `$patch: "delete"` removes the repo from effective config

### copyGlobs semantics

`copyGlobs` at every level uses **additive merge with de-duplication**, never replacement. The effective list is built by concatenating defaults → `workspace.json` → `workspace.local.json` (and, per repo, the root list → the repo's own `copyGlobs`), dropping duplicates while preserving order. Setting `copyGlobs` in a local override or repo entry extends the inherited list — it cannot remove entries from it.

### Coordination repos

A coordination repo is a directory that doesn't contain the main project code but instead contains task management files (`.rpi/`, tickets, plans) and references sibling repos through `../api`, `../web`, etc. `localPath: "."` simply refers to the selected repository itself.

### disabled field

`disabled: true` at root level makes `setup-worktree` check out the task branch instead of creating worktrees. Users can re-enable it in local overrides without touching shared config.
