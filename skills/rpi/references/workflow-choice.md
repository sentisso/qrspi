# Workflow Choice

Show this chart when asking the user which flow to use:

```text
┌──────┐
│ Task │
└──┬───┘
   │    ┌────────────────────┐    ┌──────────┐
   ├───▶│ Research questions │───▶│ Research │
   │    └────────────────────┘    └────┬─────┘
   │                                   │
   │         ┌─────────────────────────┘
   │         │    ┌──────────────────────┐
   │         ├───▶│ 1. Design discussion │────────┐
   │         │    └──────────────────────┘        │
   │         │    ┌────────┐    ┌─────┐           │
   │         └───▶│ 2. PRD │───▶│ TDD │───────────┤
   │              └────────┘    └─────┘           ▼
   │                                    ┌───────────────────┐
   │                                    │ Structure outline │
   │                                    └─────────┬─────────┘
   │                                              ▼
   │                                    ┌───────────────────┐
   │                                    │ Detailed plan     │
   │                                    │ (optional)        │
   │                                    └─────────┬─────────┘
   │                                              ▼
   │  3. Oneshot                        ┌───────────────────┐
   └───────────────────────────────────▶│ Worktree          │
                                        │ (optional)        │
                                        └─────────┬─────────┘
                                                  ▼
                                        ┌───────────────────┐    ┌────┐
                                        │ Implement         │───▶│ PR │
                                        └───────────────────┘    └────┘
```

The flows:

1. `rpi`: Medium task. Research the codebase, then settle the product and technical choices in one design discussion, then outline and implement. It fits a change where both kinds of choices fit in one document.
2. `prd`: Large feature. Research, then a PRD for the problem and the user-visible solution, then a TDD for the system and code design. You approve the PRD before the TDD starts. It fits a large feature with open product questions.
3. `oneshot`: Small and clear. Implement straight from the ticket, with no research or design documents. It fits a change whose behavior and code shape are already clear.

Recommend the shortest flow that controls the main risk. A change with unclear behavior or code shape needs a planned flow.

First print a message with the chart (use box-drawing glyphs, not Mermaid), a brief recommendation based on the request, and this note:

> Implementation can start from any workflow step. If you decide that phase's document specifies the task well enough, we can skip the rest of the workflow and get to building. Just let me know.

Then ask which flow they want. With the available tool for asking the user a multiple-choice question, give one option per flow in the order above, labeled `1. RPI`, `2. PRD-Oriented` and `3. Oneshot`, with the flow's description from the list above as the option description. Add "(Recommended)" to the recommended option's label. Without such a tool, list the three flows with their descriptions after the note and ask in plain text.
