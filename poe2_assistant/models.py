from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ItemData:
    """Normalized item data parsed from copied in-game item text."""

    raw_text: str
    name: str = ""
    base_type: str = ""
    item_class: str = ""
    rarity: str = ""
    item_level: int | None = None
    requirements: dict[str, int] = field(default_factory=dict)
    stats: dict[str, float] = field(default_factory=dict)
    implicit_mods: list[str] = field(default_factory=list)
    explicit_mods: list[str] = field(default_factory=list)


@dataclass(slots=True)
class FilterResult:
    matched: bool
    reasons: list[str] = field(default_factory=list)
