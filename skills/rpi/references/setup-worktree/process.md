---
name: setup-worktree
description: Only use when the user explicitly invokes this skill by name.
---

## steps to follow

When the task directory has a plan (`*-plan-*.md`), suggest `/rpi implement-plan <task-slug>` instead of `/rpi implement-outline <task-slug>` in every final answer below. When the task directory has neither a structure outline nor a plan, suggest `/rpi implement-direct <task-slug>` instead.

<step index=0>

### Step 0: Check if worktree setup should be skipped

First, check if workspace setup is disabled: read `.rpi/workspace.json` and `.rpi/workspace.local.json`.

<condition if="disabled is true (workspace.local.json takes precedence over workspace.json)">
Worktree setup is disabled for this project.

**Output this final answer instead of proceeding:**

First, check out the task branch for the user:

```bash
git checkout -b [BRANCHNAME]
```

Then output this final answer:

<output_example>
Workspace setup is disabled for this project (via `.rpi/workspace.json` or `.rpi/workspace.local.json`).

I've checked out branch `[BRANCHNAME]` for you. To start implementation, create a new session with the following command:

```text
/rpi implement-outline <task-slug>
```

To re-enable workspace setup, edit the file that sets `disabled: true` and change it to `false`, or add `"disabled": false` to `.rpi/workspace.local.json` to override the shared config.
</output_example>

**Do NOT proceed to Step 1 unless the user explicitly confirms they want to create a worktree anyway.**
</condition>

Next, check if you're already in a git worktree:

```bash
git rev-parse --git-dir
```

<condition if="output contains '.git/worktrees/'">
You are already inside a worktree. Creating another worktree from here is probably not what the user wants.

**Output this final answer instead of proceeding:**

<output_example>
You're already in a worktree at `[current directory]`.

To start implementation, create a new session with the following command:

```text
/rpi implement-outline <task-slug>
```

If you really do want to create a new worktree from here, let me know and I can still help with that.
</output_example>

**Do NOT proceed to Step 1 unless the user explicitly confirms they want to create a worktree anyway.**
</condition>

</step>

<step index=1>

### Step 1 Get required information

1. Figure out what task you're working on - you should have the slug to .rpi/tasks/TASKSLUG already

1a. once you have a task dir, read `.rpi/tasks/TASKSLUG/ticket.md` (or `task.md`) and the structure outline (`.rpi/tasks/TASKSLUG/...outline...md`) if present.

</step>


<step index=2>

Create the worktrees by running the setup script from the repository root:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/setup_worktree.py TASKSLUG
```

The script merges `.rpi/workspace.json` with `.rpi/workspace.local.json`, and stops with instructions for the user when the workspace is not configured. For each repo it creates the worktree, copies the `copyGlobs` files and runs the setup command. It links the worktree's `.rpi/tasks` to this checkout's `.rpi/tasks`, so the task documents stay in one place. It prints a `worktree:` line per repo, and its last line `start: <path>` is `[WORKTREE_FULL_PATH]` for the final answer.

If there are any error messages or failures, report the error to the user and work with the user to complete the setup

don't proceed to step 3 until the worktrees are created and setup is complete

</step>

<step index=3>

**Only output this if the worktree(s) were successfully created.**

If you encountered an error in Step 2, do NOT output this section.

<output_example>
Worktree for {{ TASKSLUG }} has been configured. You can start implementation by running

```text
/rpi implement-outline {{ TASKSLUG }}
```

in the [WORKTREE_FULL_PATH] directory

You can modify worktree behavior by editing the .rpi/workspace.json (committed, shared config) and .rpi/workspace.local.json (local overrides, gitignored) files.

</output_example>

</step>
