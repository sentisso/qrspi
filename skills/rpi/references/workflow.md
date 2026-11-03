# Choose a Workflow

Research establishes what exists, design settles what should change, and implementation builds the agreed result. Use the shortest path that gives the user useful review points.

## Three Flows

`rpi` and `prd` start with research questions and research. `oneshot` starts with implementation:

| Flow | Research and design | Then |
| --- | --- | --- |
| `rpi` (default) | Research, design discussion | Structure outline, detailed plan (optional), worktree (optional), implement, PR |
| `prd` | Research, PRD, TDD | Structure outline, detailed plan (optional), worktree (optional), implement, PR |
| `oneshot` | None | Worktree (optional), implement from `ticket.md`, PR |

- Design discussion combines product and technical choices in one document. It fits a change with a few clear options.
- PRD followed by TDD separates the user-facing result from the technical approach. It fits a larger feature with open product questions.
- Oneshot implements the ticket directly. It fits a copy change, a small script, or a bug with a clear cause. Use a planned flow when a wrong design would cause costly code changes.
- After the structure outline, the user chooses the next step: a detailed plan with code-level steps, a worktree, or implementation.

The user can start at any step. After research or any design step, they can skip ahead to an outline or to implementation when the documents already specify the task well enough.

## Each Phase Has a Clear Job

| Phase | Result | Review point |
| --- | --- | --- |
| Research questions | Questions about current behavior, with exact source pointers | The user can refine the scope before research |
| Research | Findings from live code and tests, without the ticket | The user can check the facts before design |
| Design discussion | Current state, desired state, options, and resolved choices | The user resolves every design question |
| PRD | Product problem, success measure, and approved solution | The user approves the product solution |
| TDD | System design, then program design | The user approves each design separately |
| Structure outline | Ordered vertical phases, each with a testable result and checks | The user reviews the scope and phase order |
| Detailed plan | Code-level changes for each outline phase | The user reviews the changes before implementation |
| Implementation | Code, tests, and a commit per phase | The user confirms manual checks before the next phase |
| PR | Pull request with description and optional walkthrough | The user reviews the code |

## Next Step

| After | Next step |
| --- | --- |
| Task start | `create-research-questions` (`rpi`, `prd`), or for `oneshot` the user's choice: `setup-worktree` when not in a worktree, or `implement-plan` |
| `create-research-questions` | `create-research` |
| `create-research` | `create-design-discussion` (`rpi`) or `create-prd` (`prd`) |
| `create-design-discussion` | `create-structure-outline`, once every design question is resolved |
| `create-prd` | `create-tech-design` |
| `create-tech-design` | `create-structure-outline` |
| `create-structure-outline` | The user's choice: `create-plan`, `setup-worktree` when not in a worktree, or `implement-outline` |
| `create-plan` | The user's choice: `setup-worktree` when not in a worktree, or `implement-plan` |
| `setup-worktree` | `implement-outline`, or `implement-plan` when a plan exists or the flow is `oneshot` |
| `implement-outline`, `implement-plan` | `describe-pr` |

An `iterate-*` step leads to the same next step as its `create-*` step.

## Documents Carry Context Between Sessions

Use a separate context window for each phase. Save current decisions, user approvals, and unfinished questions in the document before handing off. Each next command includes the task slug and chosen flow, for example:

```text
/rpi create-research ENG-1478-parent-child-tracking flow: prd
/rpi create-prd ENG-1478-parent-child-tracking flow: prd
/rpi create-structure-outline ENG-1478-parent-child-tracking
/rpi implement-outline ENG-1478-parent-child-tracking
```

Feedback updates the document that owns the choice, either in the current session or through a new `/rpi` invocation. If a document needs more work and the session is low on context, start a new session with the matching `iterate-*` step:

```text
/rpi iterate-tech-design ENG-1478-parent-child-tracking use the existing worker queue
```

When documents conflict, the later one wins: plan > structure outline > TDD > PRD > design discussion > research > ticket. For current behavior, live code wins over every document.

Documents are numbered by a zero-padded prefix in creation order:

```text
.rpi/tasks/<task-slug>/
├── ticket.md
├── 01-research-questions-<description>.md
├── 02-research-<description>.md
├── 03-design-discussion-<description>.md   # or 03-prd-<description>.md, 04-tdd-<description>.md
├── 04-structure-outline-<description>.md
├── 05-plan-<description>.md                # optional
├── mockup-*.html, diagram-*.html           # optional
└── pr-description.md, pr-walkthrough.html  # written by describe-pr
```

A `oneshot` task has only `ticket.md` and the `describe-pr` files.
