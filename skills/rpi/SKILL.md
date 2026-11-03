---
name: rpi
description: Only use when the user explicitly invokes this skill by name.
disable-model-invocation: true
argument-hint: "[step] [task-slug] [request or feedback]"
---

# Research, Design, and Implement

Help the user research a change, work through its design, and implement it. Follow their requested step, using the phase instructions below.

Paths in the phase instructions start with the CLAUDE_SKILL_DIR variable, which is this skill's directory: `${CLAUDE_SKILL_DIR}`. "The task artifact directory from your system prompt", `TASKNAME`, `TASKSLUG`, `<task slug>`, and `ENG-XXXX-description` mean the task directory selected under "Use the Task Directory".

## Choose the Step

Follow the user's requested step. Read `${CLAUDE_SKILL_DIR}/references/workflow.md` when choosing or explaining a flow or what comes next.

For a task description with no requested step, ask which flow the user wants: `rpi` (design discussion), `prd` (PRD followed by TDD) or `oneshot` (implementation from the ticket), unless the request names one. Wait for their choice before starting the phase, then carry it into suggested next commands.

When asking the user to choose a flow, read `${CLAUDE_SKILL_DIR}/references/workflow-choice.md` and follow it to show the chart and ask the question.

Create writes a new document; iterate updates an existing document in place using the user's feedback or resumes the workflow for a partially finished document.

Load the matching process from `${CLAUDE_SKILL_DIR}/references/<step>/process.md`:

| Request | Step |
| --- | --- |
| Research questions | `create-research-questions` or `iterate-research-questions` |
| Research | `create-research` or `iterate-research` |
| Design discussion | `create-design-discussion` or `iterate-design-discussion` |
| Product requirements / PRD | `create-prd` or `iterate-prd` |
| Technical design / TDD | `create-tech-design` or `iterate-tech-design` |
| Implementation outline | `create-structure-outline` or `iterate-structure-outline` |
| Detailed plan | `create-plan` or `iterate-plan` |
| Worktree setup | `setup-worktree` |
| Worktree configuration | `configure-workspaces` |
| Implement | `implement-outline`, or `implement-plan` when a plan exists or the flow is `oneshot` |
| Implementation feedback or fixes | `iterate-implementation` |
| Pull request | `describe-pr` |
| Commit | `ci-commit` |

Update an existing document by default; create one when needed or requested. When several match, use the newest and name the chosen file.

## Use the Task Directory

Use the directory supplied by the user.

Otherwise, list `.rpi/tasks/` with `ls -La` and look for task directories whose names and workflow filenames match the request or current task branch. Reuse an obvious match without asking. If a directory looks close but could belong to a different task, or several directories look plausible, ask the user which to use before writing. Read only documents allowed by the selected phase when checking a match.

When no existing directory fits, create `.rpi/tasks/<task-slug>` without asking for approval. Use the ticket ID followed by a 2-4 word kebab-case description when the request names a ticket, such as `ENG-1478-parent-child-tracking`, and a short kebab-case slug from the request otherwise. State the selected path.

If `git check-ignore -q .rpi/tasks` fails, append `/.rpi/tasks/` to `.git/info/exclude`. Do not commit the task directory.

## Write the Ticket

Write `ticket.md` only when the user starts a task with a task description: no requested step, or `create-research-questions`. Keep an existing `ticket.md` or `task.md`. Never write `ticket.md` during research, so the research stays objective about the current codebase.

Write the user's task description verbatim under a heading with the task name:

```markdown
# <Task name>

<Task description, verbatim>
```

## Implement a Oneshot Task

In the `oneshot` flow, run `implement-plan` without a subagent. There's no plan: implement `ticket.md` directly, then read the final answer template from the `implement-plan` directory and reproduce the final answer from it exactly, with its last line pointing at `ticket.md` instead of the plan.

When the user starts a `oneshot` task, write `ticket.md`, then let them choose the next step. Leave out the worktree option when `git rev-parse --git-dir` contains `.git/worktrees/`:

````markdown
The ticket has been saved to `.rpi/tasks/<task-slug>/ticket.md`. Run one of these next steps in a new session:

- **Worktree (optional):** set up an isolated worktree for the implementation.

  ```text
  /rpi setup-worktree <task-slug> flow: oneshot
  ```

- **Implement:** start building from the ticket in the current checkout.

  ```text
  /rpi implement-plan <task-slug> flow: oneshot
  ```
````

## Suggest the Next Step

Use the phase's final-answer template and `${CLAUDE_SKILL_DIR}/references/workflow.md` to choose what comes next. Users run each phase in a separate context window. When suggesting a next command, include the task slug and chosen flow. Say it's recommended to run it in a new session.

Use artifact filenames to locate the current phase when asked what's next, then read its document for unfinished work and settled choices. Tell `research-questions` files apart from `research` files. Recognize `prd` or `product-requirements`, `tdd` or `tech-design`, `structure-outline` or `outline`, and `plan`. A structure outline or plan whose phases are not all marked `✅` means implementation is unfinished. A task directory with only `ticket.md` is either a `oneshot` task or a task that has not started. Check the branch for implementation commits to tell them apart.

## Use Subagents

Use the bundled agent instructions for `codebase-analyzer`, `codebase-locator`, `codebase-pattern-finder`, `implementation-reviewer`, `implementer-agent`, `outline-implementer-agent`, and `web-search-researcher` as directed by each phase.

<important if="you have a tool for running subagents or delegated sessions, but the named subagents are not available">
  read the subagent instructions from `${CLAUDE_SKILL_DIR}/references/agents/<agent-name>.md` and pass them into the subagent with your main prompt, with
<instructions>
REFERENCE_CONTENTS
</instructions>
<message>
YOUR_MESSAGE ON WHAT TO LOOK FOR OR BUILD
</message>
</important>
