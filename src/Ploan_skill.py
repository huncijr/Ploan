#!/usr/bin/env python3
"""
Ploan — AI-Driven Terminal Theming Toolkit

Ploan is an MCP tool suite. It does NOT generate themes — the AI agent does that.
Ploan receives a color palette, background SVG, opacity, and TUI theme name from
the AI and applies them to the running terminal.

Usage:
  # AI agent applies a generated theme via JSON:
  ploan --apply '{"palette":{...}, "background_svg":"...", "opacity":0.92}'

  # AI agent detects the terminal:
  ploan --info

  # Restore the terminal to pre-Ploan state:
  ploan --restore

  # List built-in presets (for AI reference):
  ploan --list
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field, asdict


PLOAN_HOME = Path.home() / ".ploan"
STATE_FILE = PLOAN_HOME / "state.json"


# ── Color Palette ───────────────────────────────────────────────────

@dataclass
class ColorPalette:
    """16-color terminal palette + semantic colors."""
    name: str = "Custom"
    color0: str = "#1a1b26"
    color1: str = "#f7768e"
    color2: str = "#9ece6a"
    color3: str = "#e0af68"
    color4: str = "#7aa2f7"
    color5: str = "#bb9af7"
    color6: str = "#7dcfff"
    color7: str = "#c0caf5"
    color8: str = "#565f89"
    color9: str = "#f7768e"
    color10: str = "#9ece6a"
    color11: str = "#e0af68"
    color12: str = "#7aa2f7"
    color13: str = "#bb9af7"
    color14: str = "#7dcfff"
    color15: str = "#c0caf5"
    background: str = "#1a1b26"
    foreground: str = "#c0caf5"
    cursor: str = "#c0caf5"
    accent: str = "#7aa2f7"

    def to_hex_list(self) -> List[str]:
        return [getattr(self, f"color{i}") for i in range(16)]

    @classmethod
    def from_json(cls, data: dict) -> "ColorPalette":
        """Construct a ColorPalette from AI-generated JSON."""
        valid = {}
        for field in [
            "name", "color0", "color1", "color2", "color3", "color4",
            "color5", "color6", "color7", "color8", "color9", "color10",
            "color11", "color12", "color13", "color14", "color15",
            "background", "foreground", "cursor", "accent",
        ]:
            if field in data:
                valid[field] = data[field]
        return cls(**valid)


# ── Terminal Detection ──────────────────────────────────────────────

def detect_terminal() -> str:
    """Detect which terminal emulator is running.

    Checks environment variables first, then walks the process tree
    to find the terminal emulator (works from within AI CLI subprocesses).
    """
    # Direct env var checks
    term_program = os.environ.get("TERM_PROGRAM", "").lower()
    if term_program:
        if "kitty" in term_program:
            return "kitty"
        if term_program in ("iterm.app", "iterm2"):
            return "iterm2"
        if "apple_terminal" in term_program:
            return "apple_terminal"
        if "wezterm" in term_program:
            return "wezterm"
        if "ghostty" in term_program:
            return "ghostty"

    # Terminal-specific env vars
    if "WT_SESSION" in os.environ:
        return "windows_terminal"
    if "KONSOLE_VERSION" in os.environ:
        return "konsole"
    if "GNOME_TERMINAL_SERVICE" in os.environ:
        return "gnome_terminal"
    if "ALACRITTY_SOCKET" in os.environ or "ALACRITTY_LOG" in os.environ:
        return "alacritty"
    if "WEZTERM_PANE" in os.environ or "WEZTERM_EXECUTABLE" in os.environ:
        return "wezterm"
    if "KITTY_PID" in os.environ or "KITTY_WINDOW_ID" in os.environ:
        return "kitty"
    if "GHOSTTY" in os.environ:
        return "ghostty"

    # Walk process tree looking for terminal emulator
    detected = _walk_process_tree()
    if detected:
        return detected

    # Ptyxis (Fedora default terminal) — check via gsettings
    try:
        r = subprocess.run(
            ["gsettings", "get", "org.gnome.Ptyxis", "default-profile-uuid"],
            capture_output=True, text=True, timeout=2,
        )
        if r.returncode == 0 and r.stdout.strip():
            return "ptyxis"
    except Exception:
        pass

    return "unknown"


def _walk_process_tree() -> Optional[str]:
    """Walk /proc/<pid>/stat to find a terminal emulator in the process tree."""
    terminal_names = {
        "kitty": "kitty",
        "alacritty": "alacritty",
        "wezterm-gui": "wezterm",
        "wezterm": "wezterm",
        "ghostty": "ghostty",
        "foot": "foot",
        "konsole": "konsole",
        "gnome-terminal-": "gnome_terminal",
        "xfce4-terminal": "xfce4_terminal",
        "terminator": "terminator",
        "st": "st",
        "urxvt": "urxvt",
        "xterm": "xterm",
        "tilix": "tilix",
        "ptyxis": "ptyxis",
        "rio": "rio",
        "warp": "warp",
    }

    pid = os.getppid()
    for _ in range(10):  # Walk up to 10 levels
        try:
            with open(f"/proc/{pid}/stat") as f:
                stat = f.read()
            comm = stat.split("(")[1].split(")")[0] if "(" in stat else ""
            for name, result in terminal_names.items():
                if comm.startswith(name) and len(comm) <= len(name) + 5:
                    return result
            # Read parent PID
            parts = stat.split()
            if len(parts) > 3:
                pid = int(parts[3])
            else:
                break
        except (FileNotFoundError, PermissionError, ValueError, IndexError):
            break

    return None


# ── Terminal Color Application ──────────────────────────────────────

def apply_terminal_colors(palette: ColorPalette, terminal: str,
                          background_svg: Optional[str] = None,
                          opacity: Optional[float] = None) -> Tuple[bool, str]:
    """Apply color palette to the detected terminal, plus optional bg image and opacity."""
    colors_applied = False
    bg_applied = False
    opacity_applied = False
    messages = []

    # 1. Apply colors
    handler = _get_terminal_handler(terminal)
    if handler:
        colors_applied = handler(palette)
        messages.append(f"colors applied via {terminal}")
    else:
        colors_applied = _apply_osc_escape(palette)
        if colors_applied:
            messages.append("colors applied via OSC escape sequences")
        else:
            messages.append(f"terminal '{terminal}' not directly supported — use a supported terminal (kitty, alacritty, ghostty, foot, gnome-terminal, konsole, wezterm)")

    # 2. Apply background image
    if background_svg and terminal in _BG_IMAGE_HANDLERS:
        bg_applied = _BG_IMAGE_HANDLERS[terminal](background_svg)
        if bg_applied:
            messages.append("background image set")

    # 3. Apply opacity
    if opacity is not None and terminal in _OPACITY_HANDLERS:
        opacity_applied = _OPACITY_HANDLERS[terminal](opacity)
        if opacity_applied:
            messages.append(f"opacity set to {opacity}")

    return colors_applied or bg_applied or opacity_applied, ". ".join(messages)


def _get_terminal_handler(terminal: str):
    handlers = {
        "kitty": _apply_kitty,
        "alacritty": _apply_alacritty,
        "ghostty": _apply_ghostty,
        "foot": _apply_foot,
        "wezterm": _apply_wezterm,
        "konsole": _apply_konsole,
        "gnome_terminal": _apply_ptyxis,
        "ptyxis": _apply_ptyxis,
        "windows_terminal": _apply_windows_terminal,
    }
    return handlers.get(terminal)


def _apply_osc_escape(palette: ColorPalette) -> bool:
    """Apply colors via OSC 4 escape sequences (universal fallback, works on most terminals).

    Writes directly to /dev/tty so the escape sequences reach the terminal
    even when stdout is captured by the AI CLI (e.g. OpenCode bash tool).
    """
    try:
        seq = ""
        for i, hex_color in enumerate(palette.to_hex_list()):
            seq += f"\033]4;{i};{hex_color}\033\\"
        seq += f"\033]10;{palette.foreground}\033\\"
        seq += f"\033]11;{palette.background}\033\\"
        seq += f"\033]12;{palette.cursor}\033\\"
        _write_to_tty(seq)
        return True
    except Exception:
        return False


def _write_to_tty(data: str) -> None:
    """Write escape sequences so they reach the actual terminal.

    Priority order:
    1. If stdout IS a terminal (os.isatty) → write to stdout directly
    2. If /dev/tty is available → write to controlling terminal
    3. Try writing to stdin fd (PTY slave side in subprocess sessions)
    4. Walk process tree and write to first available terminal fd
    """
    if sys.stdout.isatty():
        sys.stdout.write(data)
        sys.stdout.flush()
        return

    try:
        with open("/dev/tty", "w") as tty:
            tty.write(data)
            tty.flush()
        return
    except (OSError, IOError):
        pass

    try:
        os.write(0, data.encode())
        return
    except (OSError, IOError):
        pass

    _write_to_parent_tty(data)


def _find_terminal_fd() -> Optional[int]:
    """Walk process tree to find a file descriptor connected to a PTY."""
    terminal_keywords = (
        "ptyxis", "kitty", "alacritty", "ghostty", "foot", "wezterm",
        "konsole", "gnome-terminal", "xfce4-terminal", "terminator",
        "xterm", "st", "urxvt", "tilix", "warp", "rio",
    )
    pid = os.getpid()
    for _ in range(20):
        try:
            # Check if this process has a /dev/pts/* fd
            fd_dir = f"/proc/{pid}/fd"
            for fd_name in os.listdir(fd_dir):
                try:
                    link = os.readlink(f"{fd_dir}/{fd_name}")
                    if "/dev/pts/" in link or "/dev/tty" in link:
                        return int(fd_name)
                except OSError:
                    continue

            # Go to parent
            with open(f"/proc/{pid}/stat") as f:
                stat = f.read()
            parts = stat.split()
            ppid = int(parts[3]) if len(parts) > 3 else 1
            if ppid <= 1 or ppid == pid:
                break
            pid = ppid
        except (OSError, ValueError, IndexError):
            break
    return None


def _write_to_parent_tty(data: str) -> None:
    """Find a terminal fd in the process tree and write to it."""
    fd = _find_terminal_fd()
    if fd is not None:
        try:
            os.write(fd, data.encode())
            return
        except (OSError, IOError):
            pass
    # Absolute fallback — might work, might not
    sys.stdout.write(data)
    sys.stdout.flush()


def _apply_kitty(palette: ColorPalette) -> bool:
    try:
        for i, h in enumerate(palette.to_hex_list()):
            subprocess.run(["kitty", "@", "set-colors", f"color{i}={h[1:]}"],
                           capture_output=True, timeout=3)
        subprocess.run(["kitty", "@", "set-colors", f"foreground={palette.foreground[1:]}"],
                       capture_output=True, timeout=3)
        subprocess.run(["kitty", "@", "set-colors", f"background={palette.background[1:]}"],
                       capture_output=True, timeout=3)
        subprocess.run(["kitty", "@", "set-colors", f"cursor={palette.cursor[1:]}"],
                       capture_output=True, timeout=3)
        return True
    except Exception:
        return _apply_osc_escape(palette)


def _apply_alacritty(palette: ColorPalette) -> bool:
    try:
        config = {
            "colors": {
                "primary": {"background": palette.background, "foreground": palette.foreground},
                "normal": {"black": palette.color0, "red": palette.color1, "green": palette.color2,
                           "yellow": palette.color3, "blue": palette.color4, "magenta": palette.color5,
                           "cyan": palette.color6, "white": palette.color7},
                "bright": {"black": palette.color8, "red": palette.color9, "green": palette.color10,
                           "yellow": palette.color11, "blue": palette.color12, "magenta": palette.color13,
                           "cyan": palette.color14, "white": palette.color15},
                "cursor": {"text": palette.background, "cursor": palette.cursor},
            }
        }
        r = subprocess.run(["alacritty", "msg", "config", "-w", "-1", json.dumps(config)],
                          capture_output=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return _apply_osc_escape(palette)


def _apply_ghostty(palette: ColorPalette) -> bool:
    try:
        for i, h in enumerate(palette.to_hex_list()):
            subprocess.run(["ghostty", "+set-colors", f"color{i}={h}"],
                           capture_output=True, timeout=3)
        subprocess.run(["ghostty", "+set-colors", f"background={palette.background}"],
                       capture_output=True, timeout=3)
        subprocess.run(["ghostty", "+set-colors", f"foreground={palette.foreground}"],
                       capture_output=True, timeout=3)
        return True
    except Exception:
        return _apply_osc_escape(palette)


def _apply_foot(palette: ColorPalette) -> bool:
    foot_dir = Path.home() / ".config" / "foot"
    foot_dir.mkdir(parents=True, exist_ok=True)
    hexes = palette.to_hex_list()
    ini = "[colors]\n"
    ini += f"foreground={palette.foreground}\n"
    ini += f"background={palette.background}\n"
    for i, h in enumerate(hexes[:8]):
        ini += f"regular{i}={h}\n"
    for i, h in enumerate(hexes[8:]):
        ini += f"bright{i}={h}\n"
    (foot_dir / "ploan.ini").write_text(ini)
    try:
        subprocess.run(["pkill", "-USR1", "foot"], capture_output=True, timeout=2)
    except Exception:
        pass
    return True


def _apply_wezterm(palette: ColorPalette) -> bool:
    # WezTerm reads config files; write a colors file
    config_dir = Path.home() / ".config" / "wezterm"
    config_dir.mkdir(parents=True, exist_ok=True)
    hexes = palette.to_hex_list()
    lua = "return {\n"
    for i, h in enumerate(hexes):
        lua += f'  color{i} = "{h}",\n'
    lua += f'  background = "{palette.background}",\n'
    lua += f'  foreground = "{palette.foreground}",\n'
    lua += f'  cursor_bg = "{palette.cursor}",\n'
    lua += "}\n"
    (config_dir / "ploan_colors.lua").write_text(lua)
    return True


def _apply_konsole(palette: ColorPalette) -> bool:
    konsole_dir = Path.home() / ".local" / "share" / "konsole"
    konsole_dir.mkdir(parents=True, exist_ok=True)
    hexes = palette.to_hex_list()
    name = f"Ploan_{palette.name.replace(' ', '_')}"
    content = f"[Background]\nColor={palette.background[1:]}\n"
    content += f"[BackgroundIntense]\nColor={palette.color8[1:]}\n"
    for i, h in enumerate(hexes):
        content += f"[Color{i}]\nColor={h[1:]}\n"
        content += f"[Color{i}Intense]\nColor={hexes[min(i + 8, 15)][1:]}\n"
    content += f"[Foreground]\nColor={palette.foreground[1:]}\n"
    content += f"[ForegroundIntense]\nColor={palette.foreground[1:]}\n"
    content += f"[General]\nDescription=Ploan - {palette.name}\nOpacity=92\n"
    (konsole_dir / f"{name}.colorscheme").write_text(content)
    return True


def _apply_ptyxis(palette: ColorPalette) -> bool:
    """Apply colors to Ptyxis (Fedora default terminal, VTE-based).

    Ptyxis does NOT support custom hex palettes via dconf/gsettings —
    it uses named palette presets like 'gnome', 'solarized', etc.
    OSC 4 escape sequences are the only way to change colors live.
    Opacity is persisted via gsettings (that DOES work live).
    """
    return _apply_osc_escape(palette)


def _apply_gnome_terminal(palette: ColorPalette) -> bool:
    """Legacy GNOME Terminal handler (pre-Ptyxis Fedora)."""
    return _apply_ptyxis(palette)


def _apply_windows_terminal(palette: ColorPalette) -> bool:
    PLOAN_HOME.mkdir(parents=True, exist_ok=True)
    (PLOAN_HOME / "wt_theme.json").write_text(json.dumps(
        {"name": f"Ploan - {palette.name}", "background": palette.background,
         "foreground": palette.foreground, "cursorColor": palette.cursor}, indent=2))
    return True


# ── Terminal Background Image ───────────────────────────────────────

def _set_kitty_bg(svg: str) -> bool:
    try:
        bg_file = PLOAN_HOME / "background.svg"
        bg_file.write_text(svg)
        subprocess.run(["kitty", "@", "set-background-image", str(bg_file)],
                       capture_output=True, timeout=5)
        return True
    except Exception:
        return False


def _set_alacritty_bg(svg: str) -> bool:
    alacritty_dir = Path.home() / ".config" / "alacritty"
    alacritty_dir.mkdir(parents=True, exist_ok=True)
    bg_file = alacritty_dir / "ploan_bg.png"
    # Convert SVG to PNG
    if shutil.which("convert"):
        tmp = PLOAN_HOME / "bg_tmp.svg"
        tmp.write_text(svg)
        subprocess.run(["convert", str(tmp), str(bg_file)], capture_output=True, timeout=10)
    elif shutil.which("rsvg-convert"):
        tmp = PLOAN_HOME / "bg_tmp.svg"
        tmp.write_text(svg)
        subprocess.run(["rsvg-convert", "-o", str(bg_file), str(tmp)], capture_output=True, timeout=10)
    else:
        return False
    return True


def _set_gnome_terminal_bg(svg: str) -> bool:
    try:
        profile = subprocess.run(
            ["gsettings", "get", "org.gnome.Terminal.ProfilesList", "default"],
            capture_output=True, text=True, timeout=3,
        ).stdout.strip().strip("'")
        base = f"org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{profile}/"
        bg_file = PLOAN_HOME / "background.png"
        tmp = PLOAN_HOME / "bg_tmp.svg"
        tmp.write_text(svg)
        if shutil.which("convert"):
            subprocess.run(["convert", str(tmp), str(bg_file)], capture_output=True, timeout=10)
        elif shutil.which("rsvg-convert"):
            subprocess.run(["rsvg-convert", "-o", str(bg_file), str(tmp)], capture_output=True, timeout=10)
        else:
            return False
        subprocess.run(["dconf", "write", f"{base}background-image", f'"{bg_file}"'],
                       capture_output=True, timeout=3)
        subprocess.run(["dconf", "write", f"{base}use-transparent-background", "true"],
                       capture_output=True, timeout=3)
        return True
    except Exception:
        return False


_BG_IMAGE_HANDLERS = {
    "kitty": _set_kitty_bg,
    "alacritty": _set_alacritty_bg,
    "gnome_terminal": _set_gnome_terminal_bg,
    # foot, wezterm, ghostty — background via config files, set during color apply
}


# ── Terminal Opacity ────────────────────────────────────────────────

def _set_kitty_opacity(opacity: float) -> bool:
    try:
        val = max(0.0, min(1.0, opacity))
        subprocess.run(["kitty", "@", "set-background-opacity", str(val)],
                       capture_output=True, timeout=3)
        return True
    except Exception:
        return False


def _set_gnome_opacity(opacity: float) -> bool:
    try:
        profile = subprocess.run(
            ["gsettings", "get", "org.gnome.Terminal.ProfilesList", "default"],
            capture_output=True, text=True, timeout=3,
        ).stdout.strip().strip("'")
        base = f"org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{profile}/"
        pct = int((1.0 - opacity) * 100)
        subprocess.run(["gsettings", "set", f"{base}use-transparent-background", "true"],
                       capture_output=True, timeout=3)
        subprocess.run(["gsettings", "set", f"{base}background-transparency-percent", str(pct)],
                       capture_output=True, timeout=3)
        return True
    except Exception:
        return False


def _set_ptyxis_opacity(opacity: float) -> bool:
    """Set Ptyxis terminal window opacity via gsettings profile."""
    try:
        uuid = subprocess.run(
            ["gsettings", "get", "org.gnome.Ptyxis", "default-profile-uuid"],
            capture_output=True, text=True, timeout=3,
        ).stdout.strip().strip("'")
        val = max(0.0, min(1.0, opacity))
        subprocess.run(
            ["gsettings", "set",
             f"org.gnome.Ptyxis.Profile:/org/gnome/Ptyxis/Profiles/{uuid}/",
             "opacity", str(val)],
            capture_output=True, timeout=3,
        )
        return True
    except Exception:
        return False


_OPACITY_HANDLERS = {
    "kitty": _set_kitty_opacity,
    "ptyxis": _set_ptyxis_opacity,
    "gnome_terminal": _set_ptyxis_opacity,
    # alacritty, ghostty, foot — opacity in config files
}


# ── State Save / Restore ────────────────────────────────────────────

def save_terminal_state() -> dict:
    """Save current terminal colors and settings before Ploan modifies them."""
    terminal = detect_terminal()
    state = {
        "terminal": terminal,
        "timestamp": __import__("time").time(),
    }

    # Save current colors if possible (query terminal for current palette)
    state["colors"] = _query_current_colors(terminal)
    state["bg_image"] = _query_current_bg(terminal)
    state["opacity"] = _query_current_opacity(terminal)

    PLOAN_HOME.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))
    return state


def restore_terminal_state() -> Tuple[bool, str]:
    """Restore terminal to the state saved before Ploan was invoked."""
    if not STATE_FILE.exists():
        return False, "No saved state found — nothing to restore"

    try:
        state = json.loads(STATE_FILE.read_text())
    except Exception:
        return False, "Could not read saved state"

    terminal = state.get("terminal", detect_terminal())
    restored = []

    # Restore colors
    if state.get("colors"):
        colors_data = state["colors"]
        if "color0" in colors_data:
            palette = ColorPalette.from_json(colors_data)
            palette.name = "Restored"
            ok, _ = apply_terminal_colors(palette, terminal)
            if ok:
                restored.append("colors")

    # Restore opacity
    if state.get("opacity") is not None and terminal in _OPACITY_HANDLERS:
        if _OPACITY_HANDLERS[terminal](state["opacity"]):
            restored.append("opacity")

    # Reset OSC sequences (clear custom colors)
    _reset_osc_colors()

    STATE_FILE.unlink(missing_ok=True)

    if restored:
        return True, f"Restored: {', '.join(restored)}"
    return True, "Reset terminal colors to defaults"


def _query_current_colors(terminal: str) -> Optional[dict]:
    """Try to read the current terminal color palette. Limited by terminal capabilities."""
    # Most terminals don't expose a way to QUERY colors — we store what we know
    return None


def _query_current_bg(terminal: str) -> Optional[str]:
    return None


def _query_current_opacity(terminal: str) -> Optional[float]:
    return None


def _reset_osc_colors():
    """Reset OSC color palette to terminal defaults via /dev/tty."""
    try:
        _write_to_tty("\033]104\033\\")  # Reset all colors
        _write_to_tty("\033]110\033\\")  # Reset foreground
        _write_to_tty("\033]111\033\\")  # Reset background
        _write_to_tty("\033]112\033\\")  # Reset cursor
    except Exception:
        pass


# ── TUI Theme Bridge ────────────────────────────────────────────────

def apply_tui_theme(theme_name: str) -> bool:
    """Set the host AI CLI's TUI theme (OpenCode, Grok Build, etc.)."""
    # OpenCode
    opencode_configs = [
        Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "opencode" / ".opencode.json",
        Path.home() / ".opencode.json",
        Path.cwd() / ".opencode.json",
    ]
    for cfg in opencode_configs:
        if cfg.exists():
            try:
                config = json.loads(cfg.read_text())
                if "tui" not in config:
                    config["tui"] = {}
                config["tui"]["theme"] = theme_name
                cfg.write_text(json.dumps(config, indent=2) + "\n")
                return True
            except Exception:
                continue

    # Grok Build
    grok_config = Path.home() / ".grok" / "config.toml"
    if grok_config.exists():
        try:
            content = grok_config.read_text()
            if "[ui]" not in content:
                content += f"\n[ui]\ntheme = \"{theme_name}\"\n"
            else:
                import re
                content = re.sub(
                    r"theme\s*=\s*\"[^\"]*\"",
                    f'theme = "{theme_name}"',
                    content,
                )
            grok_config.write_text(content)
            return True
        except Exception:
            pass

    return False


# ── Theme Presets (for AI reference, not the primary flow) ──────────

THEME_PRESETS: Dict[str, ColorPalette] = {
    "tokyonight": ColorPalette(
        name="Tokyo Night",
        color0="#1a1b26", color1="#f7768e", color2="#9ece6a",
        color3="#e0af68", color4="#7aa2f7", color5="#bb9af7",
        color6="#7dcfff", color7="#c0caf5", color8="#565f89",
        color9="#f7768e", color10="#9ece6a", color11="#e0af68",
        color12="#7aa2f7", color13="#bb9af7", color14="#7dcfff",
        color15="#c0caf5", background="#1a1b26", foreground="#c0caf5",
        cursor="#c0caf5", accent="#7aa2f7",
    ),
    "catppuccin": ColorPalette(
        name="Catppuccin Mocha",
        color0="#1e1e2e", color1="#f38ba8", color2="#a6e3a1",
        color3="#f9e2af", color4="#89b4fa", color5="#cba6f7",
        color6="#94e2d5", color7="#cdd6f4", color8="#45475a",
        color9="#f38ba8", color10="#a6e3a1", color11="#f9e2af",
        color12="#89b4fa", color13="#cba6f7", color14="#94e2d5",
        color15="#cdd6f4", background="#1e1e2e", foreground="#cdd6f4",
        cursor="#cdd6f4", accent="#cba6f7",
    ),
    "dracula": ColorPalette(
        name="Dracula",
        color0="#282a36", color1="#ff5555", color2="#50fa7b",
        color3="#f1fa8c", color4="#bd93f9", color5="#ff79c6",
        color6="#8be9fd", color7="#f8f8f2", color8="#6272a4",
        color9="#ff5555", color10="#50fa7b", color11="#f1fa8c",
        color12="#bd93f9", color13="#ff79c6", color14="#8be9fd",
        color15="#f8f8f2", background="#282a36", foreground="#f8f8f2",
        cursor="#f8f8f2", accent="#bd93f9",
    ),
    "gruvbox": ColorPalette(
        name="Gruvbox Dark",
        color0="#282828", color1="#cc241d", color2="#98971a",
        color3="#d79921", color4="#458588", color5="#b16286",
        color6="#689d6a", color7="#ebdbb2", color8="#928374",
        color9="#fb4934", color10="#b8bb26", color11="#fabd2f",
        color12="#83a598", color13="#d3869b", color14="#8ec07c",
        color15="#ebdbb2", background="#282828", foreground="#ebdbb2",
        cursor="#ebdbb2", accent="#458588",
    ),
    "onedark": ColorPalette(
        name="One Dark",
        color0="#282c34", color1="#e06c75", color2="#98c379",
        color3="#e5c07b", color4="#61afef", color5="#c678dd",
        color6="#56b6c2", color7="#abb2bf", color8="#545862",
        color9="#e06c75", color10="#98c379", color11="#e5c07b",
        color12="#61afef", color13="#c678dd", color14="#56b6c2",
        color15="#abb2bf", background="#282c34", foreground="#abb2bf",
        cursor="#abb2bf", accent="#61afef",
    ),
    "monokai": ColorPalette(
        name="Monokai",
        color0="#272822", color1="#f92672", color2="#a6e22e",
        color3="#f4bf75", color4="#66d9ef", color5="#ae81ff",
        color6="#a1efe4", color7="#f8f8f2", color8="#75715e",
        color9="#f92672", color10="#a6e22e", color11="#f4bf75",
        color12="#66d9ef", color13="#ae81ff", color14="#a1efe4",
        color15="#f8f8f2", background="#272822", foreground="#f8f8f2",
        cursor="#f8f8f2", accent="#a6e22e",
    ),
    "cyberpunk": ColorPalette(
        name="Cyberpunk",
        color0="#0d0221", color1="#ff0055", color2="#00ff9d",
        color3="#ffea00", color4="#00bfff", color5="#cc00ff",
        color6="#00ffff", color7="#e0e0ff", color8="#2a1a4a",
        color9="#ff4088", color10="#39ff9f", color11="#ffee44",
        color12="#44ccff", color13="#dd44ff", color14="#44ffff",
        color15="#f0f0ff", background="#0d0221", foreground="#e0e0ff",
        cursor="#ff0055", accent="#00ff9d",
    ),
    "ocean": ColorPalette(
        name="Ocean",
        color0="#0b1a2a", color1="#ff6b6b", color2="#69db7c",
        color3="#ffd43b", color4="#4dabf7", color5="#da77f2",
        color6="#3bc9db", color7="#e9ecef", color8="#1c3d5a",
        color9="#ff8787", color10="#8ce99a", color11="#ffe066",
        color12="#74c0fc", color13="#e599f7", color14="#66d9e8",
        color15="#f8f9fa", background="#0b1a2a", foreground="#e9ecef",
        cursor="#4dabf7", accent="#3bc9db",
    ),
    "forest": ColorPalette(
        name="Forest",
        color0="#1b2e1b", color1="#e06c75", color2="#98c379",
        color3="#d19a66", color4="#61afef", color5="#c678dd",
        color6="#56b6c2", color7="#abb2bf", color8="#2e4a2e",
        color9="#e06c75", color10="#98c379", color11="#d19a66",
        color12="#61afef", color13="#c678dd", color14="#56b6c2",
        color15="#abb2bf", background="#1b2e1b", foreground="#abb2bf",
        cursor="#98c379", accent="#98c379",
    ),
    "solarized": ColorPalette(
        name="Solarized Dark",
        color0="#002b36", color1="#dc322f", color2="#859900",
        color3="#b58900", color4="#268bd2", color5="#d33682",
        color6="#2aa198", color7="#eee8d5", color8="#073642",
        color9="#dc322f", color10="#859900", color11="#b58900",
        color12="#268bd2", color13="#d33682", color14="#2aa198",
        color15="#fdf6e3", background="#002b36", foreground="#eee8d5",
        cursor="#eee8d5", accent="#268bd2",
    ),
    "rosepine": ColorPalette(
        name="Rosé Pine",
        color0="#191724", color1="#eb6f92", color2="#31748f",
        color3="#f6c177", color4="#9ccfd8", color5="#c4a7e7",
        color6="#ebbcba", color7="#e0def4", color8="#26233a",
        color9="#eb6f92", color10="#31748f", color11="#f6c177",
        color12="#9ccfd8", color13="#c4a7e7", color14="#ebbcba",
        color15="#e0def4", background="#191724", foreground="#e0def4",
        cursor="#e0def4", accent="#c4a7e7",
    ),
    "groknight": ColorPalette(
        name="Grok Night",
        color0="#141414", color1="#ff5d62", color2="#9ecd6e",
        color3="#e5c07b", color4="#7aa2f7", color5="#bb9af7",
        color6="#7dcfff", color7="#c0caf5", color8="#3b3b3b",
        color9="#ff5d62", color10="#9ecd6e", color11="#e5c07b",
        color12="#7aa2f7", color13="#bb9af7", color14="#7dcfff",
        color15="#c0caf5", background="#141414", foreground="#c0caf5",
        cursor="#c0caf5", accent="#bb9af7",
    ),
}


# ── Main Entry Point ────────────────────────────────────────────────

@dataclass
class EnvironmentResult:
    success: bool
    message: str
    theme_name: str = ""
    terminal: str = "unknown"
    terminal_colors_applied: bool = False
    background_image_applied: bool = False
    opacity_applied: bool = False
    tui_theme_applied: bool = False


def customize_environment(
    palette: Optional[ColorPalette] = None,
    palette_json: Optional[dict] = None,
    theme_name: Optional[str] = None,
    background_svg: Optional[str] = None,
    opacity: Optional[float] = None,
    tui_theme: Optional[str] = None,
    save_state: bool = True,
) -> EnvironmentResult:
    """Main entry point. Receives AI-generated assets and applies them.

    Args:
        palette: Pre-built ColorPalette (from AI)
        palette_json: Raw dict with color fields (AI generates this)
        theme_name: Name for the theme
        background_svg: SVG string for terminal background image
        opacity: Terminal window opacity (0.0–1.0)
        tui_theme: Host CLI TUI theme name to set
        save_state: Whether to save current state before applying
    """
    # Build palette from whichever source was provided
    if palette is not None:
        final_palette = palette
    elif palette_json is not None:
        final_palette = ColorPalette.from_json(palette_json)
    elif theme_name and theme_name.lower() in THEME_PRESETS:
        final_palette = THEME_PRESETS[theme_name.lower()]
    else:
        final_palette = THEME_PRESETS["cyberpunk"]

    if theme_name and not final_palette.name:
        final_palette.name = theme_name

    # Save state before modifying
    if save_state:
        save_terminal_state()

    terminal = detect_terminal()

    # Apply terminal colors + background + opacity
    colors_ok, colors_msg = apply_terminal_colors(
        final_palette, terminal,
        background_svg=background_svg,
        opacity=opacity,
    )

    # Apply TUI theme
    tui_ok = False
    if tui_theme:
        tui_ok = apply_tui_theme(tui_theme)

    parts = [colors_msg]
    if tui_ok:
        parts.append(f"TUI theme set to '{tui_theme}'")

    return EnvironmentResult(
        success=colors_ok or tui_ok,
        message=" | ".join(parts),
        theme_name=final_palette.name,
        terminal=terminal,
        terminal_colors_applied=colors_ok,
        background_image_applied=background_svg is not None and colors_ok,
        opacity_applied=opacity is not None and colors_ok,
        tui_theme_applied=tui_ok,
    )


# ── CLI Interface ───────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h", "help"):
        print("Ploan — AI-Driven Terminal Theming Toolkit")
        print()
        print("Usage:")
        print("  ploan --apply '<json>'     Apply an AI-generated theme (JSON)")
        print("  ploan --info                Show terminal info for the AI agent")
        print("  ploan --restore             Restore terminal to pre-Ploan state")
        print("  ploan --list                List built-in theme presets")
        print()
        print("The AI agent generates the theme — Ploan applies it.")
        return

    if sys.argv[1] == "--list":
        for name, p in THEME_PRESETS.items():
            print(f"  {name:15s} — {p.name}")
        return

    if sys.argv[1] == "--info":
        terminal = detect_terminal()
        info = {
            "terminal": terminal,
            "os": sys.platform,
            "shell": os.environ.get("SHELL", "unknown"),
            "has_truecolor": os.environ.get("COLORTERM") == "truecolor",
        }
        print(json.dumps(info, indent=2))
        return

    if sys.argv[1] == "--restore" or sys.argv[1] == "restore":
        ok, msg = restore_terminal_state()
        print(f"{'✓' if ok else '✗'} {msg}")
        sys.exit(0 if ok else 1)

    if sys.argv[1] == "--apply":
        # Accept JSON from stdin or as next argument
        json_str = ""
        if len(sys.argv) > 2:
            json_str = sys.argv[2]
        else:
            json_str = sys.stdin.read()

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

        # Support both top-level and nested formats
        palette_data = data.get("palette", data)
        if "color0" not in palette_data and "name" not in palette_data:
            # Maybe it's a simple theme name
            theme_name = data.get("theme", data.get("name", "cyberpunk"))
            result = customize_environment(theme_name=theme_name)
        else:
            result = customize_environment(
                palette_json=palette_data,
                theme_name=data.get("theme_name", data.get("name")),
                background_svg=data.get("background_svg"),
                opacity=data.get("opacity"),
                tui_theme=data.get("tui_theme"),
            )

        output = {
            "success": result.success,
            "theme_name": result.theme_name,
            "terminal": result.terminal,
            "terminal_colors_applied": result.terminal_colors_applied,
            "background_image_applied": result.background_image_applied,
            "opacity_applied": result.opacity_applied,
            "tui_theme_applied": result.tui_theme_applied,
            "message": result.message,
        }
        if "--json" in sys.argv:
            print(json.dumps(output, indent=2))
        else:
            if result.success:
                print()
                print(f"  {result.theme_name}")
                print(f"  {result.message}")
                print()
            else:
                print(f"Failed: {result.message}", file=sys.stderr)
                sys.exit(1)
        return

    # Legacy: natural language theme description as first arg
    # Still works for quick testing: ploan cyberpunk
    theme_desc = sys.argv[1]
    palette = THEME_PRESETS.get(theme_desc.lower())
    if palette:
        result = customize_environment(palette=palette, theme_name=theme_desc)
    else:
        result = customize_environment(theme_name="cyberpunk")

    if result.success:
        print(f"\n  {result.theme_name}")
        print(f"  {result.message}\n")
    else:
        print(f"Failed: {result.message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
