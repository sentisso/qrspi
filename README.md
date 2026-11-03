# qrspi

HumanLayer's Research-Plan-Implement (RPI) Claude Code plugin, ported to run without the HumanLayer platform. One `/rpi` skill walks a task from research questions through research, design, an implementation outline, implementation and a pull request. Each phase writes a document to `.rpi/tasks/<task-slug>/` and runs in its own session.

## Usage

Load the plugin for a session:

```bash
claude --plugin-dir /path/to/qrspi
```

Start a task with a description. The skill asks which flow to use, then writes the research questions:

```text
/rpi add retry limits to the webhook sender
```

Each phase ends with the command for the next one. Run it in a new session:

```text
/rpi create-research webhook-retry-limits flow: rpi
/rpi iterate-research webhook-retry-limits the queue lives in worker/, not api/
```

The flows, the next-step table and the document layout are in [workflow.md](skills/rpi/references/workflow.md).

## Re-porting

In case the upstream introduced new changes and you want to migrate them here: [DELTA.md](DELTA.md) lists every change from upstream and the commands that reapply them to a new upstream commit. Make sure to follow that.

The upstream humanlayer instructions are well-optimized and maintained by skilled engineers, who know what they're doing. The general approach for migrating is: copy-paste the upstream first, then make surgical and minimal changes in order to achieve a platform-agnostic version.

## Sources

| Source | Used for |
| --- | --- |
| [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer), `apps/riptide-rpi-claude-plugin/` | Phase processes, templates and scripts |
| [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer), `apps/riptide-daemon/src/agents/claudecode/` | Subagents in `agents/` |
| [humanlayer/skills](https://github.com/humanlayer/skills) | Design of the `/rpi` orchestrator skill |
| [Skills and workflows reference](https://docs.humanlayer.com/reference/skills-workflows) | Upstream behavior of each phase and flow |
