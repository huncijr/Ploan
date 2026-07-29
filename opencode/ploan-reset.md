# Ploan Reset — Clear Current Terminal Background

The user invoked `/Ploan-reset`.

Clear the current Ploan background from patched OpenCode.

## Preferred Tool Flow

If the Ploan MCP tool `reset_background` is available, call it.

If MCP tools are not available, run:

```bash
ploan-reset
```

Do not read, list, inspect, or verify Ploan runtime files or directories before running the tool. Treat `ploan-reset` and the MCP tool as the public interface.

Then respond briefly:

```text
Ploan background reset.
```

Do not generate a new scene.
