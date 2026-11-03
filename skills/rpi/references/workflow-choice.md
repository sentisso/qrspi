# Workflow Choice

Show this chart when asking the user which flow to use:

```text
┌────────────────────┐    ┌──────────┐
│ Research questions │───▶│ Research │
└────────────────────┘    └────┬─────┘
                               │
     ┌─────────────────────────┘
     │    ┌─────────────────────────┐
     ├───▶│ 1, 3. Design discussion │───────┐
     │    └─────────────────────────┘       │
     │    ┌────────┐    ┌─────┐             │
     └───▶│ 2. PRD │───▶│ TDD │─────────────┤
          └────────┘    └─────┘             ▼
                                ┌───────────────────┐    ┌──────────────────┐
                                │ Structure outline │───▶│ 3. Detailed plan │
                                └─────────┬─────────┘    └────────┬─────────┘
                                          ▼                       │
                                ┌───────────────────┐             │
                                │ Worktree          │◀────────────┘
                                │ (optional)        │
                                └─────────┬─────────┘
                                          ▼
                                ┌───────────────────┐    ┌────┐
                                │ Implement         │───▶│ PR │
                                └───────────────────┘    └────┘
```

1. `rpi`: Design discussion settles product and technical choices in one document. It fits a change with a few clear options.
2. `prd`: PRD followed by TDD separates the user-facing result from the technical approach. It fits a larger feature with open product questions.
3. `plan`: Design discussion, then a detailed plan with code-level steps after the structure outline. It fits a change the user wants specified down to the code before implementation.

Briefly recommend a flow based on the request, then ask which they prefer. Use box-drawing glyphs, not Mermaid.

Include this note with the chart and recommendation:

> Implementation can start from any workflow step. If you decide that phase's document specifies the task well enough, we can skip the rest of the workflow and get to building. Let me know.
