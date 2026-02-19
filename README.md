# PoE2 Crafting Assistant (Python Rewrite)

This repository has been rewritten as a **Python-first Path of Exile 2 helper**.

## What changed

The original Java app targeted PoE1 and automated in-game behavior. This rewrite focuses on a safer, scriptable workflow for PoE2:

- Parse copied PoE2 item text into structured fields.
- Evaluate items against JSON filters.
- Return a simple **HIT/MISS** result with reasons.

> This version intentionally avoids mouse/keyboard automation.

## Quick start

### 1) Run directly with Python

```bash
python -m poe2_assistant.cli --item-file examples/poe2_item.txt --filter-file examples/poe2_filter.json
```

### 2) Optional install as a CLI

```bash
pip install -e .
poe2-assistant --item-file examples/poe2_item.txt --filter-file examples/poe2_filter.json
```

## Filter format

Example filter (`examples/poe2_filter.json`):

```json
{
  "rarity": "Rare",
  "item_class": "Quarterstaves",
  "min_item_level": 75,
  "include_mods": ["to Maximum Life"],
  "exclude_mods": ["reduced Attack Speed"],
  "stat_thresholds": {
    "to_maximum_life": 80
  }
}
```

### Supported keys

- `rarity` (exact match, case-insensitive)
- `item_class` (exact match, case-insensitive)
- `min_item_level` (numeric minimum)
- `include_mods` (all substrings must appear in parsed mods)
- `exclude_mods` (none of the substrings may appear)
- `stat_thresholds` (normalized stat-name to minimum numeric value)

## Development

Run tests:

```bash
python -m pytest
```

## Notes

- PoE2 item text formats are evolving. The parser is intentionally permissive so you can adapt filter logic quickly.
- If you want, the next step can be adding a small desktop UI (PySide/Tkinter) on top of this core.
