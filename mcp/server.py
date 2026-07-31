#!/usr/bin/env python3
"""
Ploan MCP Server — exposes terminal visual-surface tools to AI agents.

The AI agent generates ASCII/Unicode/ANSI scenes, palettes, dashboards,
and optional CSS. Ploan renders those visible surfaces and can optionally
apply matching terminal palette changes.

MCP Protocol: JSON-RPC 2.0 over stdio.

Compatible with: OpenCode, Claude Code, Grok Build, open-interpreter.
"""

import json
import sys
import os
import traceback
import shutil
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from Ploan_skill import (
    customize_environment,
    detect_terminal,
    restore_terminal_state,
    apply_terminal_colors,
    save_terminal_state,
    THEME_PRESETS,
    ColorPalette,
    render_scene,
    analyze_scene_quality,
    render_dashboard,
    save_background,
    reset_background,
)

MCP_VERSION = "2024-11-05"
SERVER_NAME = "ploan"
SERVER_VERSION = "0.2.0"


def log(msg: str) -> None:
    print(f"[ploan-mcp] {msg}", file=sys.stderr, flush=True)


def send_response(response: dict) -> None:
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()


def handle_initialize(msg_id: Any, params: dict) -> None:
    send_response({
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {
            "protocolVersion": MCP_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {
                "name": SERVER_NAME,
                "version": SERVER_VERSION,
            },
        },
    })


def handle_list_tools(msg_id: Any) -> None:
    send_response({
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {
            "tools": [
                {
                    "name": "render_scene",
                    "description": (
                        "Render an AI-generated terminal background using ASCII, "
                        "Unicode box drawing, Braille/half-block art, ANSI colors, "
                        "gradients, and ambient full-width composition. This is the primary Ploan tool: "
                        "the user should see image-like background art, not only 'theme applied'."
                    ),
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "scene": {
                                "type": "object",
                                "description": "Scene object with image-like ASCII/Unicode art lines. Use no_text=true for backgrounds unless the user asks for words.",
                                "properties": {
                                    "title": {"type": "string"},
                                    "subtitle": {"type": "string"},
                                    "kind": {"type": "string"},
                                    "no_text": {"type": "boolean"},
                                    "include_text": {"type": "boolean"},
                                    "full_width": {"type": "boolean"},
                                    "width": {"type": "number"},
                                    "background_width": {"type": "number"},
                                    "background_height": {"type": "number"},
                                    "composition": {"type": "string"},
                                    "subject": {"type": "string"},
                                    "reference_style": {"type": "string"},
                                    "rendering_mode": {"type": "string"},
                                    "quality_target": {"type": "string"},
                                    "subject_priority": {"type": "string"},
                                    "light_source": {"type": "string"},
                                    "density": {"type": "string"},
                                    "focal_strength": {"type": "string"},
                                    "palette": {"type": "object"},
                                    "lines": {"type": "array", "items": {"type": "string"}},
                                },
                                "required": ["lines"],
                            },
                            "plain": {
                                "type": "boolean",
                                "description": "Strip ANSI colors and render plain Unicode fallback.",
                                "default": False,
                            },
                            "target": {
                                "type": "string",
                                "description": "Host background target to update when a patched host is available: opencode or codex.",
                                "enum": ["opencode", "codex"],
                                "default": "opencode",
                            },
                        },
                        "required": ["scene"],
                    },
                },
                {
                    "name": "render_dashboard",
                    "description": "Render a framed terminal dashboard or themed prompt banner.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "palette": {"type": "object"},
                            "width": {"type": "number"},
                            "cards": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "label": {"type": "string"},
                                        "value": {"type": "string"},
                                    },
                                },
                            },
                            "plain": {"type": "boolean", "default": False},
                            "target": {
                                "type": "string",
                                "description": "Host background target to update when a patched host is available: opencode or codex.",
                                "enum": ["opencode", "codex"],
                                "default": "opencode",
                            },
                        },
                    },
                },
                {
                    "name": "customize_environment",
                    "description": (
                        "Apply a terminal theme generated by the AI agent. "
                        "The AI provides a complete color palette, optional "
                        "SVG background image, opacity value, and TUI theme name. "
                        "Ploan applies these to the running terminal, TUI, and Web UI. "
                        "Use get_terminal_info first to detect the terminal type and "
                        "capabilities before generating the theme assets."
                    ),
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "scene": {
                                "type": "object",
                                "description": "Optional visual surface scene. If provided, Ploan renders it first.",
                            },
                            "palette": {
                                "type": "object",
                                "description": (
                                    "Complete 16-color ANSI palette with semantic colors. "
                                    "Fields: name (string), color0 through color15 (hex strings like '#1a1b26'), "
                                    "background (hex), foreground (hex), cursor (hex), accent (hex). "
                                    "Generate these colors based on the user's theme description."
                                ),
                                "properties": {
                                    "name": {"type": "string"},
                                    "color0": {"type": "string"}, "color1": {"type": "string"},
                                    "color2": {"type": "string"}, "color3": {"type": "string"},
                                    "color4": {"type": "string"}, "color5": {"type": "string"},
                                    "color6": {"type": "string"}, "color7": {"type": "string"},
                                    "color8": {"type": "string"}, "color9": {"type": "string"},
                                    "color10": {"type": "string"}, "color11": {"type": "string"},
                                    "color12": {"type": "string"}, "color13": {"type": "string"},
                                    "color14": {"type": "string"}, "color15": {"type": "string"},
                                    "background": {"type": "string"},
                                    "foreground": {"type": "string"},
                                    "cursor": {"type": "string"},
                                    "accent": {"type": "string"},
                                },
                            },
                            "background_svg": {
                                "type": "string",
                                "description": (
                                    "SVG markup to render as the terminal background image. "
                                    "Keep it simple and abstract — ~800x600, matching the theme's energy. "
                                    "Use gradients that blend with the background color."
                                ),
                            },
                            "opacity": {
                                "type": "number",
                                "description": "Terminal window opacity (0.0 = transparent, 1.0 = solid). Typical range: 0.85-0.95.",
                            },
                            "tui_theme": {
                                "type": "string",
                                "description": (
                                    "TUI theme name to set for the host AI CLI. "
                                    "For OpenCode: one of 'opencode', 'catppuccin', 'dracula', 'flexoki', "
                                    "'gruvbox', 'monokai', 'onedark', 'tokyonight', 'tron'. "
                                    "For Grok Build: one of 'groknight', 'grokday', 'tokyonight', "
                                    "'rosepine-moon', 'oscura-midnight', 'auto'."
                                ),
                            },
                            "theme_name": {
                                "type": "string",
                                "description": "Human-readable name for the generated theme (e.g. 'Cyberpunk Ocean').",
                            },
                            "save_state": {
                                "type": "boolean",
                                "description": "Save current terminal state before applying (for restore). Default: true.",
                                "default": True,
                            },
                            "apply_terminal_palette": {
                                "type": "boolean",
                                "description": "Whether to mutate terminal palette in addition to rendering the visible scene.",
                                "default": False,
                            },
                            "plain": {
                                "type": "boolean",
                                "description": "Render scene without ANSI colors.",
                                "default": False,
                            },
                            "target": {
                                "type": "string",
                                "description": "Host background target to update when a patched host is available: opencode or codex.",
                                "enum": ["opencode", "codex"],
                                "default": "opencode",
                            },
                        },
                    },
                },
                {
            "name": "reset_background",
                    "description": "Clear the current patched host Ploan background layer.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "string",
                                "description": "Host background target to reset: opencode or codex.",
                                "enum": ["opencode", "codex"],
                                "default": "opencode",
                            },
                        },
                    },
                },
                {
                    "name": "get_terminal_info",
                    "description": (
                        "Detect the current terminal emulator, OS, and color support level. "
                        "The AI should call this BEFORE generating a theme, so the generated "
                        "assets are compatible with the user's terminal capabilities."
                    ),
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                    },
                },
                {
                    "name": "restore_environment",
                    "description": (
                        "Restore the terminal to its state before the last Ploan theme was applied. "
                        "Resets colors, background image, and opacity to their original values."
                    ),
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                    },
                },
                {
                    "name": "list_themes",
                    "description": (
                        "List built-in theme presets the AI can use as starting points "
                        "or reference when generating custom palettes."
                    ),
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                    },
                },
            ],
        },
    })


def handle_call_tool(msg_id: Any, tool_name: str, arguments: dict) -> None:
    try:
        if tool_name == "render_scene":
            rendered = render_scene(arguments, plain=arguments.get("plain", False))
            save_background(rendered, arguments, target=arguments.get("target", "opencode"))
            quality = analyze_scene_quality(arguments, target=arguments.get("target", "opencode"))
            text = rendered
            text += "\nPLOAN_QUALITY_FEEDBACK\n"
            text += json.dumps(quality, indent=2)
            send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"content": [{"type": "text", "text": text}]},
            })

        elif tool_name == "render_dashboard":
            rendered = render_dashboard(arguments, plain=arguments.get("plain", False))
            save_background(rendered, target=arguments.get("target", "opencode"))
            send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"content": [{"type": "text", "text": rendered}]},
            })

        elif tool_name == "reset_background":
            removed = reset_background(arguments.get("target", "opencode"))
            send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": "Ploan background reset." if removed else "Ploan background already clear."}],
                },
            })

        elif tool_name == "get_terminal_info":
            terminal = detect_terminal()
            info = {
                "terminal": terminal,
                "width": shutil.get_terminal_size((80, 24)).columns,
                "os": sys.platform,
                "shell": os.environ.get("SHELL", "unknown"),
                "has_truecolor": os.environ.get("COLORTERM") == "truecolor",
                "supported_terminals_for_background_image": [
                    "kitty", "alacritty", "gnome_terminal",
                ],
                "supported_terminals_for_opacity": [
                    "kitty", "gnome_terminal",
                ],
                "supported_terminals_for_colors": [
                    "kitty", "alacritty", "ghostty", "foot", "wezterm",
                    "konsole", "gnome_terminal", "windows_terminal",
                ],
                "note": (
                    "If terminal is 'unknown', the server is running in a subprocess "
                    "(e.g. from an AI CLI tool). Colors can still be applied via OSC "
                    "escape sequences on most terminals."
                ),
            }
            send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"content": [{"type": "text", "text": json.dumps(info, indent=2)}]},
            })

        elif tool_name == "customize_environment":
            scene_data = arguments.get("scene")
            palette_data = arguments.get("palette")
            background_svg = arguments.get("background_svg")
            opacity = arguments.get("opacity")
            tui_theme = arguments.get("tui_theme")
            theme_name = arguments.get("theme_name")
            save_state = arguments.get("save_state", True)
            apply_terminal_palette = arguments.get("apply_terminal_palette", bool(palette_data))
            plain = arguments.get("plain", False)
            target = arguments.get("target", "opencode")

            log(f"Applying theme: {theme_name or 'custom'} (tui={tui_theme}, opacity={opacity})")

            rendered_scene = ""
            if scene_data:
                scene_input = {"scene": scene_data}
                rendered_scene = render_scene(scene_input, plain=plain)
                save_background(rendered_scene, scene_input, target=target)
                quality = analyze_scene_quality(scene_input, target=target)
                rendered_scene += "\nPLOAN_QUALITY_FEEDBACK\n"
                rendered_scene += json.dumps(quality, indent=2)
                rendered_scene += "\n"

            if scene_data and not apply_terminal_palette and not palette_data and not tui_theme:
                send_response({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": rendered_scene}]},
                })
                return

            if scene_data and apply_terminal_palette and not palette_data:
                semantic = scene_data.get("palette", {})
                bg = semantic.get("background", "#080012")
                fg = semantic.get("foreground", "#e8e8ff")
                accent = semantic.get("accent", "#00f5ff")
                secondary = semantic.get("secondary", "#ff2bd6")
                warning = semantic.get("warning", "#b7ff00")
                palette_data = {
                    "name": scene_data.get("title", "Ploan Scene"),
                    "color0": bg, "color1": secondary, "color2": accent,
                    "color3": warning, "color4": accent, "color5": secondary,
                    "color6": accent, "color7": fg, "color8": bg,
                    "color9": secondary, "color10": accent, "color11": warning,
                    "color12": accent, "color13": secondary, "color14": accent,
                    "color15": fg, "background": bg, "foreground": fg,
                    "cursor": accent, "accent": accent,
                }

            result = customize_environment(
                palette_json=palette_data,
                theme_name=theme_name,
                background_svg=background_svg,
                opacity=opacity,
                tui_theme=tui_theme,
                save_state=save_state,
            )

            text = rendered_scene
            text += f"**{result.theme_name}**\n\n"
            text += f"- Terminal: `{result.terminal}` — "
            if result.terminal_colors_applied:
                text += "colors applied\n"
            else:
                text += "colors applied via OSC fallback\n"

            if result.background_image_applied:
                text += "- Background image set\n"
            if result.opacity_applied:
                text += f"- Opacity set to {opacity}\n"
            if result.tui_theme_applied:
                text += f"- TUI theme set to `{tui_theme}`\n"

            text += f"\n{result.message}"

            send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"content": [{"type": "text", "text": text}]},
            })

        elif tool_name == "restore_environment":
            log("Restoring terminal state...")
            ok, msg = restore_terminal_state()
            send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"content": [{"type": "text", "text": f"{'✓' if ok else '✗'} {msg}"}]},
            })

        elif tool_name == "list_themes":
            themes_list = "\n".join(
                f"- **{name}** — {palette.name} "
                f"(bg: {palette.background}, fg: {palette.foreground}, accent: {palette.accent})"
                for name, palette in THEME_PRESETS.items()
            )
            send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": (
                            "Built-in Ploan theme presets (use as reference or starting points):\n\n"
                            f"{themes_list}\n\n"
                            "When generating a custom palette, use these color schemes as inspiration "
                            "but create your own unique colors based on the user's description."
                        ),
                    }],
                },
            })

        else:
            send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            })

    except Exception as e:
        log(f"Error calling tool {tool_name}: {e}")
        log(traceback.format_exc())
        send_response({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [{"type": "text", "text": f"Error: {e}"}],
                "isError": True,
            },
        })


def handle_notifications(method: str) -> bool:
    if method in ("notifications/initialized", "initialized"):
        log("MCP initialized successfully")
        return True
    return False


def main():
    log("Ploan MCP server v0.2.0 starting...")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            log(f"Invalid JSON received: {line[:100]}")
            continue

        msg_id = msg.get("id")
        method = msg.get("method", "")
        params = msg.get("params", {})

        if method == "initialize":
            handle_initialize(msg_id, params)
        elif method == "tools/list":
            handle_list_tools(msg_id)
        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            handle_call_tool(msg_id, tool_name, arguments)
        elif handle_notifications(method):
            pass
        elif msg_id is not None:
            send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            })
        else:
            log(f"Ignoring unknown notification: {method}")


if __name__ == "__main__":
    main()
