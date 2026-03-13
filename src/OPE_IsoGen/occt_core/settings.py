from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import os
import tomllib  # Python 3.11+

# -----------------------------
# Dataclasses for typed settings
# -----------------------------
@dataclass
class ProjectSettings:
    name: str = "OPE-IsoGen"
    units: str = "mm"
    strict_mode: bool = True

@dataclass
class IOSettings:
    output_dir: str = "out"
    svg_chord_mm: float = 20.0
    overwrite: bool = True

@dataclass
class IsoSettings:
    xy_scale: float = 1.0
    z_scale: float = 1.0
    deg30_cos: float = 0.866025403784  # cos(30°)
    deg30_sin: float = 0.5             # sin(30°)

@dataclass
class StepExportSettings:
    enabled: bool = True
    filename: str = "pipeline.step"

@dataclass
class SvgExportSettings:
    enabled: bool = True
    filename: str = "pipeline.svg"
    stroke_width: int = 2
    padding: float = 20.0

@dataclass
class ExportSettings:
    # IMPORTANT: use default_factory for nested dataclasses
    step: StepExportSettings = field(default_factory=StepExportSettings)
    svg: SvgExportSettings  = field(default_factory=SvgExportSettings)

@dataclass
class DebugSettings:
    log_level: str = "info"
    print_bounds: bool = False

@dataclass
class Settings:
    # IMPORTANT: use default_factory for all nested dataclasses
    project: ProjectSettings = field(default_factory=ProjectSettings)
    io: IOSettings           = field(default_factory=IOSettings)
    isometric: IsoSettings   = field(default_factory=IsoSettings)
    export: ExportSettings   = field(default_factory=ExportSettings)
    debug: DebugSettings     = field(default_factory=DebugSettings)

# -----------------------------
# Loader / merger
# -----------------------------
def _deep_get(d: dict, path: list[str], default=None):
    cur = d
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur

def _merge_dataclass(dc, src: dict, path: list[str]):
    """Assign values from src dict into a dataclass (1-level deep per section)."""
    for field_name in dc.__dataclass_fields__.keys():  # type: ignore[attr-defined]
        val = _deep_get(src, path + [field_name], None)
        if val is not None:
            setattr(dc, field_name, val)

def load_settings(path: Optional[str] = None) -> Settings:
    """
    Load settings from TOML file.
    Precedence:
      1) explicit `path` if provided
      2) env var OPEISOGEN_SETTINGS
      3) default: settings/default_settings.toml
    """
    candidates = []
    if path:
        candidates.append(path)
    env_path = os.getenv("OPEISOGEN_SETTINGS")
    if env_path:
        candidates.append(env_path)
    candidates.append(os.path.join("settings", "default_settings.toml"))

    file_to_use = None
    for p in candidates:
        if p and os.path.isfile(p):
            file_to_use = p
            break

    settings = Settings()  # defaults
    if not file_to_use:
        print("[INFO] No settings TOML found; using in-code defaults.")
        return settings

    with open(file_to_use, "rb") as f:
        data = tomllib.load(f)

    # Merge section by section
    _merge_dataclass(settings.project, data, ["project"])
    _merge_dataclass(settings.io, data, ["io"])
    _merge_dataclass(settings.isometric, data, ["isometric"])
    if "export" in data:
        _merge_dataclass(settings.export.step, data, ["export", "step"])
        _merge_dataclass(settings.export.svg, data, ["export", "svg"])
    _merge_dataclass(settings.debug, data, ["debug"])

    print(f"[OK] Loaded settings: {file_to_use}")
    return settings