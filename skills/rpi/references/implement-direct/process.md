# Implementation Without an Outline

You are the orchestrator for implementing a task from `.rpi/tasks/` that has no structure outline or plan: a `oneshot` task, or a task the user takes to implementation straight after research or a design step. The `rpi:oneshot-implementer-agent` subagent does the implementation in one run.

## Getting Started

When invoked:
1. Discover documents in the task directory with `ls -La .rpi/tasks/TASKNAME`. Do NOT use Glob or Grep, as the directory may be a symlink.
2. If the directory has a plan (`*-plan-*.md`), stop and suggest `/rpi implement-plan <task-slug>`. If it has a structure outline (`*-structure-outline-*.md`), stop and suggest `/rpi implement-outline <task-slug>`.
3. Otherwise, follow the workflow below.

## Workflow

### 1. Launch Implementer Agent

Use the **Agent tool** with `subagent_type="rpi:oneshot-implementer-agent"`. Provide the task directory and the paths of ALL the task documents you discovered.

Example prompt:
```
Implement the task in .rpi/tasks/ENG-XXXX-description

Documents:
- Ticket: .rpi/tasks/ENG-XXXX-description/ticket.md
- Research: .rpi/tasks/ENG-XXXX-description/02-research-DESCRIPTION.md
- Design discussion: .rpi/tasks/ENG-XXXX-description/03-design-discussion-DESCRIPTION.md

Implement the whole change and run the repository's standard checks.
```

IMPORTANT — keep your prompt short. The implementer agent will read the documents itself. Do not duplicate the document contents in your prompt.

### 2. Report to Human

```
## Implementation Summary

**What was done:**
- [Brief summary of changes]

**Automated verification results:**
- [Results of the checks you ran]

**Manual verification needed:**
- [Manual checks from the documents, or none]
```

### 3. Wait for Human Confirmation

Ask for the human to:
- Confirm manual checks passed
- Report any issues found

### 4. Commit the Changes

- Create a commit for the changes
- Remember — the `.rpi/tasks/` directory should not be committed

### Handling Issues

If the implementer agent reports a mismatch or gets stuck:
- Present the issue clearly to the human
- Wait for guidance before proceeding
- Consider whether the outline needs to be updated based on codebase evolution

## After Completion

1. Read the final output template:

Read `${CLAUDE_SKILL_DIR}/references/implement-plan/references/implement_plan_final_answer.md`

2. Respond following the template exactly, with its last line pointing at the newest document the implementation used instead of the plan. Do not include a summary or other information.
