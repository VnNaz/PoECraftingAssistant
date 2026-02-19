from __future__ import annotations

import re

from .models import ItemData

STAT_RE = re.compile(r"(?P<value>[+-]?\d+(?:\.\d+)?)%?\s+(?P<name>.+)")


def _normalize_key(name: str) -> str:
    return (
        name.lower()
        .replace("%", "percent")
        .replace("+", "plus")
        .replace("-", "minus")
        .replace(" ", "_")
    )


def parse_item_text(text: str) -> ItemData:
    """Parse PoE2 copied item text into a structured object.

    The parser is permissive: unknown lines are preserved in explicit_mods.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    item = ItemData(raw_text=text)

    if not lines:
        return item

    index = 0
    if lines and lines[0].startswith("Rarity:"):
        item.rarity = lines[0].split(":", 1)[1].strip()
        index = 1

    divider_indexes = [i for i, line in enumerate(lines) if line == "--------"]
    header_end = divider_indexes[0] if divider_indexes else len(lines)
    header_lines = lines[:header_end]

    for i, line in enumerate(header_lines):
        if line.startswith("Rarity:"):
            item.rarity = line.split(":", 1)[1].strip()
            if i + 1 < len(header_lines):
                item.name = header_lines[i + 1]
            if i + 2 < len(header_lines):
                item.base_type = header_lines[i + 2]
            break

    if not item.name and index < len(lines):
        item.name = lines[index]
        index += 1
    if not item.base_type and index < len(lines):
        item.base_type = lines[index]

    for line in lines:
        if line.startswith("Item Class:"):
            item.item_class = line.split(":", 1)[1].strip()
        elif line.startswith("Item Level:"):
            try:
                item.item_level = int(line.split(":", 1)[1].strip())
            except ValueError:
                item.item_level = None
        elif ":" in line and line.split(":", 1)[0] in {"Level", "Str", "Dex", "Int"}:
            req_key, req_value = line.split(":", 1)
            req_value = req_value.strip()
            if req_value.isdigit():
                item.requirements[req_key.lower()] = int(req_value)
        elif line.startswith("{ Implicit Modifier"):
            continue
        elif line.startswith("{ Prefix Modifier") or line.startswith("{ Suffix Modifier"):
            continue
        else:
            stat_match = STAT_RE.match(line)
            if stat_match:
                value = float(stat_match.group("value"))
                name = stat_match.group("name").strip()
                item.stats[_normalize_key(name)] = value

            if "(implicit)" in line.lower():
                item.implicit_mods.append(line)
            elif any(token in line for token in ["to ", "increased", "more", "less", "resistance"]):
                item.explicit_mods.append(line)

    return item
