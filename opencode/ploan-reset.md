# Ploan Reset — Clear Current Terminal Background

The user invoked `/Ploan-reset`.

Clear the current Ploan background from patched OpenCode.

## Preferred Tool Flow

If the Ploan MCP tool `reset_background` is available, call it.

If MCP tools are not available, run:

```bash
python3 ~/.ploan/src/Ploan_skill.py --reset
```

Then respond briefly:

```text
Ploan background reset.
```

Do not generate a new scene.
