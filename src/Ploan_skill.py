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

  # Render AI-generated visible terminal art:
  ploan --render-scene '{"scene":{"title":"...","lines":[...]}}'

  # Demo visible terminal art:
  ploan --demo cyberpunk

  # List built-in presets (for AI reference):
  ploan --list
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
import re
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field, asdict


PLOAN_HOME = Path.home() / ".ploan"
STATE_FILE = PLOAN_HOME / "state.json"
OPENCODE_BACKGROUND_FILE = PLOAN_HOME / "opencode" / "background.txt"


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
        color0="#0a0014", color1="#ff006e", color2="#00ff88",
        color3="#ffe600", color4="#00d4ff", color5="#d600ff",
        color6="#00fff5", color7="#d4d4ff", color8="#1a0a33",
        color9="#ff3388", color10="#26ffa0", color11="#fff033",
        color12="#33ddff", color13="#e633ff", color14="#33fff7",
        color15="#f0f0ff", background="#0a0014", foreground="#d4d4ff",
        cursor="#ff006e", accent="#00ff88",
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


# ── Terminal Visual Surface Renderer ───────────────────────────────

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _normalize_hex(hex_color: Optional[str], fallback: str = "#ffffff") -> str:
    if not hex_color:
        return fallback
    value = str(hex_color).strip()
    if not value.startswith("#"):
        value = f"#{value}"
    if len(value) != 7:
        return fallback
    try:
        int(value[1:], 16)
    except ValueError:
        return fallback
    return value.lower()


def hex_to_rgb(hex_color: Optional[str], fallback: str = "#ffffff") -> Tuple[int, int, int]:
    value = _normalize_hex(hex_color, fallback)
    return int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16)


def fg(hex_color: Optional[str]) -> str:
    r, g, b = hex_to_rgb(hex_color)
    return f"\033[38;2;{r};{g};{b}m"


def bg(hex_color: Optional[str]) -> str:
    r, g, b = hex_to_rgb(hex_color)
    return f"\033[48;2;{r};{g};{b}m"


def reset() -> str:
    return "\033[0m"


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


def visible_len(text: str) -> int:
    return len(strip_ansi(text))


def fit_width(line: str, width: int) -> str:
    plain = strip_ansi(line)
    if len(plain) <= width:
        return line
    # Keep this conservative; truncating ANSI-aware strings safely is more work,
    # so truncation is only applied before coloring in renderer paths.
    return plain[:width]


def pad_visible(line: str, width: int) -> str:
    return line + (" " * max(0, width - visible_len(line)))


def gradient_text(text: str, colors: List[str], plain: bool = False) -> str:
    if plain or not colors:
        return text
    if len(colors) == 1:
        return f"{fg(colors[0])}{text}{reset()}"
    chars = list(text)
    if not chars:
        return ""
    out = []
    segments = max(1, len(colors) - 1)
    for i, ch in enumerate(chars):
        t = i / max(1, len(chars) - 1)
        pos = min(segments - 1, int(t * segments))
        local = (t * segments) - pos
        r1, g1, b1 = hex_to_rgb(colors[pos])
        r2, g2, b2 = hex_to_rgb(colors[pos + 1])
        r = int(r1 + (r2 - r1) * local)
        g = int(g1 + (g2 - g1) * local)
        b = int(b1 + (b2 - b1) * local)
        out.append(f"\033[38;2;{r};{g};{b}m{ch}")
    out.append(reset())
    return "".join(out)


def render_swatches(palette: dict, plain: bool = False) -> str:
    keys = ["background", "accent", "secondary", "warning", "foreground"]
    colors = [_normalize_hex(palette.get(k), "#ffffff") for k in keys if palette.get(k)]
    if not colors:
        colors = ["#080012", "#00f5ff", "#ff2bd6", "#b7ff00", "#e8e8ff"]
    if plain:
        return "  ".join(colors)
    return "  ".join(f"{bg(c)}  {reset()} {c}" for c in colors)


def _scene_palette(scene: dict) -> dict:
    palette = scene.get("palette") or {}
    return {
        "background": _normalize_hex(palette.get("background"), "#080012"),
        "foreground": _normalize_hex(palette.get("foreground"), "#e8e8ff"),
        "accent": _normalize_hex(palette.get("accent"), "#00f5ff"),
        "secondary": _normalize_hex(palette.get("secondary"), "#ff2bd6"),
        "warning": _normalize_hex(palette.get("warning"), "#b7ff00"),
        **{k: v for k, v in palette.items() if k not in {"background", "foreground", "accent", "secondary", "warning"}},
    }


def _default_scene(theme: str = "cyberpunk") -> dict:
    theme = theme.lower().strip()
    if "ocean" in theme or "abyss" in theme or "bio" in theme:
        return {
            "title": "ABYSSAL BLOOM",
            "subtitle": "bioluminescent terminal surface",
            "width": 72,
            "palette": {
                "background": "#061826",
                "foreground": "#e0ffff",
                "accent": "#00e5ff",
                "secondary": "#39ffbf",
                "warning": "#7dd3fc",
            },
            "lines": [
                "╔════════════════════════════════════════════════════════════╗",
                "║  PLOAN // ABYSSAL BLOOM                                   ║",
                "╠════════════════════════════════════════════════════════════╣",
                "║  ░▒▓ deep current / bioluminescent haze / silent pressure ▓▒░ ║",
                "║                                                            ║",
                "║        ⣀⣤⣶⣿⣿⣶⣤⣀        teal light under glass       ║",
                "║     ⣴⣿⠟⠋⠁  ⠈⠙⠻⣿⣦   drifting code current        ║",
                "║     ⣿⡇   ▄▄  ▄▄   ⢸⣿   cyan plankton sparks         ║",
                "║     ⠻⣿⣦⣀      ⣀⣴⣿⠟                              ║",
                "║                                                            ║",
                "║  #061826   #00e5ff   #39ffbf   #7dd3fc   #e0ffff          ║",
                "╚════════════════════════════════════════════════════════════╝",
            ],
        }
    if "ship" in theme or "space" in theme or "saturn" in theme or "cockpit" in theme:
        return {
            "title": "ORBITAL COCKPIT",
            "subtitle": "starship dashboard terminal surface",
            "width": 72,
            "palette": {
                "background": "#050713",
                "foreground": "#e6f1ff",
                "accent": "#66e3ff",
                "secondary": "#ffb86b",
                "warning": "#f8f871",
            },
            "lines": [
                "╔════════════════════════════════════════════════════════════╗",
                "║  PLOAN // ORBITAL COCKPIT                                 ║",
                "╠════════════════════════════════════════════════════════════╣",
                "║   SATURN VECTOR  ░░░░░░░░░░░░░░░░░░░░  SYSTEMS NOMINAL    ║",
                "║                                                            ║",
                "║      .        *      .        ________        *      .     ║",
                "║   *       .        .      ___/  ____  \\___       .         ║",
                "║        .       *         /___  /____\\  ___\\          *     ║",
                "║    NAV ▣▣▣▣▣▣▣   THRUST ▣▣▣▣▣░░   SHIELD ▣▣▣▣▣▣    ║",
                "║                                                            ║",
                "║  #050713   #66e3ff   #ffb86b   #f8f871   #e6f1ff          ║",
                "╚════════════════════════════════════════════════════════════╝",
            ],
        }
    return {
        "title": "NIGHT CITY MODE",
        "subtitle": "cyberpunk 2077 terminal visual surface",
        "width": 72,
        "palette": {
            "background": "#080012",
            "foreground": "#e8e8ff",
            "accent": "#00f5ff",
            "secondary": "#ff2bd6",
            "warning": "#b7ff00",
        },
        "lines": [
            "╔════════════════════════════════════════════════════════════╗",
            "║  PLOAN // NIGHT CITY MODE                                 ║",
            "╠════════════════════════════════════════════════════════════╣",
            "║  ░▒▓ neon skyline / scanline haze / chrome rain ▓▒░        ║",
            "║                                                            ║",
            "║        ▄▄      ▄████▄         ▄▄       NEON GRID           ║",
            "║     ▄██▀▀██▄  ██▀  ▀██     ▄██▀▀██▄    // 2077            ║",
            "║     ██ CYBER ██ █▓▒░ ██     ██ GRID ██   SIGNAL HOT       ║",
            "║     ▀██▄▄██▀  ██▄▄▄▄██     ▀██▄▄██▀    RAIN IN STATIC    ║",
            "║                                                            ║",
            "║  #080012   #ff2bd6   #00f5ff   #b7ff00   #e8e8ff          ║",
            "╚════════════════════════════════════════════════════════════╝",
        ],
    }


def render_scene(scene_input: dict, plain: bool = False) -> str:
    """Render an AI-generated terminal visual surface.

    The scene can be passed either as {"scene": {...}} or directly as a scene dict.
    """
    scene = scene_input.get("scene", scene_input) if isinstance(scene_input, dict) else {}
    if not scene:
        scene = _default_scene("cyberpunk")
    palette = _scene_palette(scene)
    background_mode = bool(scene.get("kind") == "background" or scene.get("no_text") or scene.get("full_width"))
    width = int(scene.get("background_width") or scene.get("width") or shutil.get_terminal_size((80, 24)).columns or 80)
    width = max(40, min(240 if background_mode else 120, width))
    title = str(scene.get("title") or "PLOAN")
    subtitle = str(scene.get("subtitle") or "AI-generated terminal visual surface")
    lines = [str(line) for line in scene.get("lines") or []]
    if not lines:
        lines = _default_scene(title).get("lines", [])

    accent = palette["accent"]
    secondary = palette["secondary"]
    foreground = palette["foreground"]
    warning = palette["warning"]
    gradient = [secondary, accent, warning]

    rendered: List[str] = []
    if background_mode:
        pass
    elif not plain:
        rendered.append(gradient_text(f"╭─ PLOAN / {title} ", gradient, plain=False) + reset())
        rendered.append(f"{fg(foreground)}│ {subtitle}{reset()}")
    else:
        rendered.append(f"PLOAN / {title}")
        rendered.append(f"{subtitle}")

    for raw in lines:
        plain_line = strip_ansi(raw)
        if len(plain_line) > width:
            plain_line = plain_line[:width]
        if plain:
            rendered.append(plain_line)
            continue
        if any(ch in plain_line for ch in "╔╚╠╣╦╩═║╭╮╰╯─│┌┐└┘"):
            rendered.append(gradient_text(plain_line, gradient, plain=False))
        elif any(ch in plain_line for ch in "█▄▀▓▒░⣿⣶⠿"):
            rendered.append(f"{fg(accent)}{plain_line}{reset()}")
        else:
            rendered.append(f"{fg(foreground)}{plain_line}{reset()}")

    if not background_mode:
        swatches = render_swatches(palette, plain=plain)
        rendered.append(("Palette: " if plain else f"{fg(foreground)}Palette:{reset()} ") + swatches)
    return "\n".join(rendered) + "\n"


def analyze_scene_quality(scene_input: dict) -> dict:
    """Return objective feedback so an AI agent can redraw weak ASCII scenes."""
    scene = scene_input.get("scene", scene_input) if isinstance(scene_input, dict) else {}
    source_lines = [strip_ansi(str(line)) for line in scene.get("lines") or []]
    width = int(scene.get("background_width") or scene.get("width") or max([len(line) for line in source_lines] or [80]))
    width = max(40, min(240, width))
    height = int(scene.get("background_height") or max(len(source_lines), 16))
    height = max(12, min(80, height))
    include_text = bool(scene.get("include_text") or scene.get("text") or scene.get("labels"))
    body = _unframe_scene_lines(source_lines, allow_text=include_text, preserve_blank=True)
    line_count = len(body)
    normalized = [line[:width].ljust(width) for line in body]
    points = [
        (row, column, char)
        for row, line in enumerate(normalized)
        for column, char in enumerate(line)
        if not char.isspace()
    ]
    issues: List[str] = []
    suggestions: List[str] = []

    caption_lines = [line.strip() for line in body if _looks_like_caption(line.strip())]
    if caption_lines and not include_text:
        issues.append("contains_readable_text")
        suggestions.append("Remove titles, labels, captions, palette lines, and debug text from scene.lines.")

    if line_count > height:
        issues.append("canvas_overflow")
        suggestions.append("Make scene.lines exactly fit background_height; extra rows are clipped from the persisted OpenCode background.")
    elif line_count < int(height * 0.75):
        issues.append("canvas_underfilled")
        suggestions.append("Use the full requested canvas height with intentional sky, midground, subject, and foreground rows.")

    if not points:
        return {
            "score": 0,
            "passed": False,
            "issues": ["empty_scene"],
            "suggestions": ["Redraw with a recognizable silhouette and at least several meaningful art rows."],
            "metrics": {"width": width, "height": height, "non_space": 0},
        }

    min_row = min(row for row, _, _ in points)
    max_row = max(row for row, _, _ in points)
    min_col = min(column for _, column, _ in points)
    max_col = max(column for _, column, _ in points)
    bbox_width = max_col - min_col + 1
    bbox_height = max_row - min_row + 1
    non_space = len(points)
    density = non_space / max(1, bbox_width * bbox_height)
    center_x = (min_col + max_col) / 2
    center_y = (min_row + max_row) / 2
    center_offset_x = abs(center_x - (width - 1) / 2) / width
    center_offset_y = abs(center_y - (height - 1) / 2) / height
    non_empty_rows = sum(1 for line in normalized if line.strip())
    bottom_start = max(0, int(height * 0.78))
    bottom_points = sum(1 for row, _, _ in points if row >= bottom_start)
    bottom_usage = bottom_points / max(1, non_space)
    strong_chars = sum(1 for _, _, char in points if char in "#@%&MW█▓▒░▀▄/\\|()[]{}<>_=-~*+oO0◯●○◌◍◎╱╲─═│ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    shaded_chars = sum(1 for _, _, char in points if char in "@%#8&WM0OQGCJft1i;:,..░▒▓█")
    unique_chars = len({char for _, _, char in points})
    outline_chars = sum(1 for _, _, char in points if char in "/\\|()[]{}<>_=-~^`'\".,╱╲─═│")
    sparse_shade_chars = sum(1 for _, _, char in points if char in ".,:;i!lI`'")
    mid_shade_chars = sum(1 for _, _, char in points if char in "tfLCJUYXzcvunxrjoahkbdpqwmZO0Q")
    dense_shade_chars = sum(1 for _, _, char in points if char in "@$#%8&WMN█▓▒░")
    ramp_classes = sum(1 for count in (outline_chars, sparse_shade_chars, mid_shade_chars, dense_shade_chars) if count > 0)
    ramp_diversity = ramp_classes / 4
    interior_points = sum(1 for row, column, _ in points if min_row < row < max_row and min_col < column < max_col)
    interior_texture_ratio = interior_points / max(1, non_space)
    bbox_area = bbox_width * bbox_height
    subject_prominence = min(1.0, bbox_area / max(1, width * height * 0.28))
    safe_top = min(height - 1, 5)
    safe_bottom = min(height - 1, 16)
    safe_left = int(width * 0.28)
    safe_right = int(width * 0.72)
    safe_zone_points = sum(1 for row, column, _ in points if safe_top <= row <= safe_bottom and safe_left <= column <= safe_right)
    safe_zone_overlap = safe_zone_points / max(1, non_space)
    classic_ascii_score = int(max(0, min(100, (
        min(1.0, shaded_chars / max(1, non_space) / 0.35) * 28
        + ramp_diversity * 24
        + min(1.0, interior_texture_ratio / 0.45) * 22
        + min(1.0, unique_chars / 16) * 16
        + min(1.0, non_empty_rows / 12) * 10
    ))))

    if non_space < 35:
        issues.append("too_sparse")
        suggestions.append("Use more contour and shading characters so the subject survives dim background rendering.")
    if non_empty_rows < 5:
        issues.append("too_few_art_rows")
        suggestions.append("Use at least 5-8 meaningful rows for a small object, or 16+ rows for a scene.")
    if bbox_width > bbox_height * 8 and bbox_height < 8:
        issues.append("too_flat_or_line_like")
        suggestions.append("Make the subject taller and more compact; avoid a thin horizontal smear.")
    if density < 0.05:
        issues.append("too_diffuse")
        suggestions.append("Concentrate the main subject into a clearer silhouette instead of scattering tiny marks.")
    if strong_chars / max(1, non_space) < 0.45:
        issues.append("weak_visual_weight")
        suggestions.append("Use stronger outline characters such as /, \\, _, -, =, |, (), #, @, block, or box drawing.")

    descriptor = " ".join(str(scene.get(key, "")) for key in ("title", "subtitle", "subject", "style", "composition", "safe_zone", "reference_style", "rendering_mode", "quality_target", "subject_priority")).lower()
    centered_requested = any(word in descriptor for word in ("center", "centered", "centre", "kozep", "közép"))
    focal_high = str(scene.get("focal_strength", "")).lower() == "high"
    single_subject = "single" in descriptor or "object" in descriptor or focal_high
    if single_subject and non_space >= 40 and (shaded_chars / max(1, non_space) < 0.18 or unique_chars < 8):
        issues.append("weak_depth_shading")
        suggestions.append("Add 3D volume: use character-density shading, internal texture bands, and asymmetric highlights/shadows instead of only outlines.")
    classic_requested = any(word in descriptor for word in ("classic", "ascii-gallery", "volumetric", "shaded-ascii"))
    if classic_requested and classic_ascii_score < 75:
        issues.append("weak_classic_ascii_craft")
        suggestions.append("Redraw with classic ASCII craft: richer density ramps, internal texture, asymmetric highlights, and old-school shading letters/numbers without copying external art.")
    if (focal_high or "foreground" in descriptor) and subject_prominence < 0.12:
        issues.append("weak_subject_prominence")
        suggestions.append("Make the requested subject larger or more foreground-dominant; reduce background detail that competes with it.")
    if not centered_requested and safe_zone_overlap > 0.45 and (focal_high or "foreground" in descriptor):
        issues.append("safe_zone_overlap")
        suggestions.append("Move the focal subject away from the OpenCode logo/input safe zone or lower it into the foreground.")
    landscape_requested = any(word in descriptor for word in ("landscape", "forest", "woods", "cabin", "house", "haz", "ház", "erdo", "erdő"))
    if landscape_requested:
        if bottom_usage < 0.08:
            issues.append("bottom_underused")
            suggestions.append("Use the lower foreground for ground, path, grass, shadows, roots, rocks, or water so the image does not stop in the middle.")
        if max_row < int(height * 0.82):
            issues.append("foreground_missing")
            suggestions.append("Extend the landscape into the lower rows with visible terrain and foreground detail.")
        if any(word in descriptor for word in ("house", "cabin", "haz", "ház")):
            house_rows = [
                row for row, line in enumerate(normalized[:height])
                if sum(1 for char in line if char in "#@%M8▓▒░|_/\\[]{}=+-") >= 18
                and int(width * 0.25) <= _line_center(line) <= int(width * 0.75)
            ]
            if not house_rows:
                issues.append("house_not_prominent")
                suggestions.append("Make the central house/cabin larger and clearer, with roof, walls, windows, door, and shading.")
            else:
                house_bottom = max(house_rows)
                ground_rows = normalized[min(height, house_bottom + 1): min(height, house_bottom + 5)]
                if not any(any(char in row for char in "_~^.:,;░▒▓#M8/\\") for row in ground_rows):
                    issues.append("subject_not_grounded")
                    suggestions.append("Place visible ground/path/grass directly below the house so it sits in the landscape instead of floating or being clipped.")
    if centered_requested and center_offset_x > 0.12:
        issues.append("not_centered_horizontally")
        suggestions.append("Move the main subject closer to the horizontal center of the canvas.")
    if centered_requested and center_offset_y > 0.22:
        issues.append("not_centered_vertically")
        suggestions.append("Move the main subject closer to the requested vertical center, unless avoiding the OpenCode prompt area.")

    theme_text = " ".join(str(scene.get(key, "")) for key in ("title", "subtitle", "subject", "style")).lower()
    if "saturn" in theme_text or "szaturn" in theme_text:
        art_text = "\n".join(normalized)
        ring_marks = sum(art_text.count(char) for char in "=-_~─═")
        planet_marks = sum(art_text.count(char) for char in "()oO0◯●○◌◍◎#@")
        if ring_marks < 12 or (planet_marks < 1 and bbox_height < 5):
            issues.append("saturn_not_recognizable")
            suggestions.append("Redraw Saturn as a compact round planet crossed by a clear elliptical ring, with the ring visible both left and right.")

    score = 100
    score -= len(set(issues)) * 12
    if density < 0.08:
        score -= 8
    if non_space < 60:
        score -= 8
    if bbox_height < 6:
        score -= 10
    if "weak_depth_shading" in issues:
        score -= 8
    if "weak_classic_ascii_craft" in issues:
        score -= 10
    if "weak_subject_prominence" in issues:
        score -= 10
    if "safe_zone_overlap" in issues:
        score -= 8
    if "canvas_overflow" in issues:
        score -= 24
    if "canvas_underfilled" in issues:
        score -= 12
    if "bottom_underused" in issues:
        score -= 10
    if "foreground_missing" in issues:
        score -= 12
    if "house_not_prominent" in issues or "subject_not_grounded" in issues:
        score -= 12
    if centered_requested:
        score -= int((center_offset_x + center_offset_y) * 30)
    score = max(0, min(100, score))

    return {
        "score": score,
        "passed": score >= 72 and not {"empty_scene", "contains_readable_text", "saturn_not_recognizable", "weak_depth_shading", "weak_classic_ascii_craft", "weak_subject_prominence", "safe_zone_overlap", "canvas_overflow", "canvas_underfilled", "bottom_underused", "foreground_missing", "house_not_prominent", "subject_not_grounded"}.intersection(issues),
        "issues": issues,
        "suggestions": suggestions[:6],
        "metrics": {
            "width": width,
            "height": height,
            "line_count": line_count,
            "non_space": non_space,
            "non_empty_rows": non_empty_rows,
            "bbox_width": bbox_width,
            "bbox_height": bbox_height,
            "density": round(density, 3),
            "shaded_ratio": round(shaded_chars / max(1, non_space), 3),
            "unique_chars": unique_chars,
            "classic_ascii_score": classic_ascii_score,
            "ramp_diversity": round(ramp_diversity, 3),
            "interior_texture_ratio": round(interior_texture_ratio, 3),
            "subject_prominence": round(subject_prominence, 3),
            "safe_zone_overlap": round(safe_zone_overlap, 3),
            "bottom_usage": round(bottom_usage, 3),
            "center_offset_x": round(center_offset_x, 3),
            "center_offset_y": round(center_offset_y, 3),
        },
    }


def render_opencode_background(scene_input: dict) -> str:
    """Render a full-screen character-art canvas for patched OpenCode.

    Chat/tool output can be framed and explanatory; the OpenCode layer should be
    ambient background art, so this strips simple box frames and pads to the
    current terminal width.
    """
    scene = scene_input.get("scene", scene_input) if isinstance(scene_input, dict) else {}
    if not scene:
        scene = _default_scene("cyberpunk")

    terminal = shutil.get_terminal_size((160, 40))
    width = int(scene.get("background_width") or scene.get("width") or terminal.columns or 180)
    width = max(60, min(240, width))
    height = int(scene.get("background_height") or terminal.lines or 40)
    height = max(16, min(80, height))

    source_lines = [strip_ansi(str(line)) for line in scene.get("lines") or []]
    if not source_lines:
        source_lines = [strip_ansi(str(line)) for line in _default_scene(str(scene.get("title") or "cyberpunk")).get("lines", [])]

    include_text = bool(scene.get("include_text") or scene.get("text") or scene.get("labels"))
    body = _unframe_scene_lines(source_lines, allow_text=include_text, preserve_blank=True)
    palette = _scene_palette(scene)
    art = body
    if include_text:
        title = str(scene.get("title") or "PLOAN")
        subtitle = str(scene.get("subtitle") or "AI-generated terminal visual surface")
        swatches = "  ".join(palette[key] for key in ["background", "accent", "secondary", "warning", "foreground"])
        art = [f"PLOAN / {title}", subtitle, "", *body, "", swatches]
    art = [line[: max(1, width)] for line in art]
    full_width = bool(scene.get("full_width") or any(len(line) >= width * 0.75 for line in art))
    if not full_width:
        while art and not art[0].strip():
            art.pop(0)
        while art and not art[-1].strip():
            art.pop()
    top = max(0 if full_width else 1, (height - len(art)) // 3)

    canvas = []
    for row in range(height):
        base = _ambient_background_line(width, row)
        index = row - top
        if 0 <= index < len(art):
            line = art[index]
            if full_width:
                base = line.ljust(width)[:width]
            else:
                left = max(0, (width - len(line)) // 2)
                base = base[:left] + line + base[min(width, left + len(line)):]
        canvas.append(base[:width])
    if full_width:
        return "\n".join(canvas) + "\n"
    return "\n".join(canvas).rstrip() + "\n"


def _unframe_scene_lines(lines: List[str], allow_text: bool = False, preserve_blank: bool = False) -> List[str]:
    content = [line.rstrip() for line in lines]
    if len(content) >= 2 and content[0].lstrip().startswith(("╔", "┌")) and content[-1].lstrip().startswith(("╚", "└")):
        content = content[1:-1]

    unframed = []
    for line in content:
        stripped = line.strip()
        if preserve_blank and not stripped:
            unframed.append("")
            continue
        if stripped.startswith(("╠", "├")):
            continue
        if stripped.startswith(("║", "│")) and stripped.endswith(("║", "│")) and len(stripped) > 2:
            stripped = stripped[1:-1].strip()
        if not allow_text and _looks_like_caption(stripped):
            continue
        unframed.append(line if preserve_blank else stripped)
    return unframed if preserve_blank else [line for line in unframed if line]


def _looks_like_caption(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if re.search(r"#[0-9a-fA-F]{6}", line):
        return True
    if re.search(r"\b(ploan|palette|mood|theme|background|terminal|caption|title|debug)\b", stripped, re.IGNORECASE):
        return True
    if re.search(r"[0-9@#\[\]/\\_~^`;.,:(){}<>|=+*\-]", stripped):
        return False
    words = re.findall(r"[A-Za-z]{3,}", stripped)
    if words and sum(len(word) for word in words) >= max(3, len(stripped.replace(" ", "")) * 0.75):
        return True
    return False


def _line_center(line: str) -> int:
    columns = [index for index, char in enumerate(line) if not char.isspace()]
    if not columns:
        return 0
    return (columns[0] + columns[-1]) // 2


def _ambient_background_line(width: int, row: int) -> str:
    chars = []
    for column in range(width):
        if (column + row * 7) % 53 == 0:
            chars.append("·")
        elif row % 6 == 0 and column % 31 < 4:
            chars.append("░")
        elif row % 11 == 0 and column > width - 18 and column % 3 == 0:
            chars.append("▒")
        else:
            chars.append(" ")
    return "".join(chars)


def save_opencode_background(rendered_scene: str, scene_input: Optional[dict] = None) -> None:
    """Persist the latest visual surface for patched OpenCode builds.

    Patched OpenCode reads this file from its OpenTUI render tree and paints it
    as a low-z-index character-art background layer.
    """
    OPENCODE_BACKGROUND_FILE.parent.mkdir(parents=True, exist_ok=True)
    OPENCODE_BACKGROUND_FILE.write_text(render_opencode_background(scene_input) if scene_input else rendered_scene)


def reset_opencode_background() -> bool:
    """Remove the current patched OpenCode background file."""
    if OPENCODE_BACKGROUND_FILE.exists():
        OPENCODE_BACKGROUND_FILE.unlink()
        return True
    return False


def render_dashboard(layout: dict, plain: bool = False) -> str:
    """Render a simple framed dashboard from layout/card data."""
    title = layout.get("title", "PLOAN DASHBOARD")
    palette = layout.get("palette", {})
    cards = layout.get("cards", [])
    width = int(layout.get("width", 72))
    width = max(40, min(120, width))
    border = "═" * (width - 2)
    lines = [f"╔{border}╗", f"║ {title[:width-4].ljust(width-4)} ║", f"╠{border}╣"]
    for card in cards:
        label = str(card.get("label", "item"))
        value = str(card.get("value", ""))
        content = f" {label}: {value}"
        lines.append(f"║ {content[:width-4].ljust(width-4)} ║")
    lines.append(f"╚{border}╝")
    return render_scene({"scene": {"title": title, "palette": palette, "width": width, "lines": lines}}, plain=plain)


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
        print("Ploan — AI-Generated Terminal Visual Surfaces")
        print()
        print("Usage:")
        print("  ploan --render-scene '<json>'  Render AI-generated terminal art")
        print("  ploan --analyze-scene '<json>'  Score an AI-generated ASCII scene")
        print("  ploan --demo cyberpunk         Render a demo visual surface")
        print("  ploan --apply '<json>'         Composite: render scene + optional palette")
        print("  ploan --reset                 Clear the current OpenCode background")
        print("  ploan --info                   Show terminal info for the AI agent")
        print("  ploan --restore                Restore terminal palette state")
        print("  ploan --list                   List built-in reference palettes")
        print()
        print("The AI agent creates the art — Ploan renders it.")
        return

    if sys.argv[1] == "--list":
        for name, p in THEME_PRESETS.items():
            print(f"  {name:15s} — {p.name}")
        return

    if sys.argv[1] in ("--reset", "--reset-background", "reset", "reset-background"):
        removed = reset_opencode_background()
        print("Ploan background reset." if removed else "Ploan background already clear.")
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

    if sys.argv[1] == "--render-scene":
        plain = "--plain" in sys.argv
        json_args = [arg for arg in sys.argv[2:] if arg != "--plain"]
        json_str = json_args[0] if json_args else sys.stdin.read()
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Invalid scene JSON: {e}", file=sys.stderr)
            sys.exit(1)
        rendered = render_scene(data, plain=plain)
        save_opencode_background(rendered, data)
        print(rendered, end="")
        return

    if sys.argv[1] == "--analyze-scene":
        json_str = sys.argv[2] if len(sys.argv) > 2 else sys.stdin.read()
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Invalid scene JSON: {e}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(analyze_scene_quality(data), indent=2))
        return

    if sys.argv[1] == "--demo":
        theme = sys.argv[2] if len(sys.argv) > 2 else "cyberpunk"
        plain = "--plain" in sys.argv
        data = {"scene": _default_scene(theme)}
        rendered = render_scene(data, plain=plain)
        save_opencode_background(rendered, data)
        print(rendered, end="")
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

        # If a scene is present, render it first. This is the new primary flow.
        if "scene" in data:
            rendered = render_scene(data, plain="--plain" in sys.argv)
            save_opencode_background(rendered, data)
            print(rendered, end="")
            if "palette" not in data and not data.get("apply_terminal_palette", False):
                return
            if "palette" not in data and data.get("apply_terminal_palette", False):
                semantic = _scene_palette(data.get("scene", {}))
                data["palette"] = {
                    "name": data.get("scene", {}).get("title", "Ploan Scene"),
                    "color0": semantic["background"],
                    "color1": semantic["secondary"],
                    "color2": semantic["accent"],
                    "color3": semantic["warning"],
                    "color4": semantic["accent"],
                    "color5": semantic["secondary"],
                    "color6": semantic["accent"],
                    "color7": semantic["foreground"],
                    "color8": semantic["background"],
                    "color9": semantic["secondary"],
                    "color10": semantic["accent"],
                    "color11": semantic["warning"],
                    "color12": semantic["accent"],
                    "color13": semantic["secondary"],
                    "color14": semantic["accent"],
                    "color15": semantic["foreground"],
                    "background": semantic["background"],
                    "foreground": semantic["foreground"],
                    "cursor": semantic["accent"],
                    "accent": semantic["accent"],
                }

        # Support both top-level and nested palette formats
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
