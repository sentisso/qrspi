# Workflow Choice

Show this chart when asking the user which flow to use:

```text
┌────────────────────┐    ┌──────────┐
│ Research questions │───▶│ Research │
└────────────────────┘    └────┬─────┘
                               │
     ┌─────────────────────────┘
     │    ┌──────────────────────┐
     ├───▶│ 1. Design discussion │──────────┐
     │    └──────────────────────┘          │
     │    ┌────────┐    ┌─────┐             │
     └───▶│ 2. PRD │───▶│ TDD │─────────────┤
          └────────┘    └─────┘             ▼
                                ┌───────────────────┐
                                │ Structure outline │
                                └─────────┬─────────┘
                                          ▼
                                ┌───────────────────┐
                                │ Worktree          │
                                │ (optional)        │
                                └─────────┬─────────┘
                                          ▼
                                ┌───────────────────┐    ┌────┐
                                │ Implement         │───▶│ PR │
                                └───────────────────┘    └────┘
```

1. Design discussion settles product and technical choices in one document. It fits a change with a few clear options.
2. PRD followed by TDD separates the user-facing result from the technical approach. It fits a larger feature with open product questions.

Briefly recommend a flow based on the request, then ask which they prefer. Use box-drawing glyphs, not Mermaid.

Include this note with the chart and recommendation:

> Implementation can start from any workflow step. If you decide that phase's document specifies the task well enough, just let me know and we can skip the rest of the workflow and get to building.
