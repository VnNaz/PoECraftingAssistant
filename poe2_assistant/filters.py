from __future__ import annotations

from .models import FilterResult, ItemData


def evaluate_filter(item: ItemData, filter_config: dict) -> FilterResult:
    """Evaluate an ItemData object against a JSON-serializable filter config."""
    reasons: list[str] = []

    rarity = filter_config.get("rarity")
    if rarity and item.rarity.lower() != rarity.lower():
        return FilterResult(False, [f"rarity mismatch: expected {rarity}, got {item.rarity or 'unknown'}"])

    item_class = filter_config.get("item_class")
    if item_class and item.item_class.lower() != item_class.lower():
        return FilterResult(False, [f"item_class mismatch: expected {item_class}, got {item.item_class or 'unknown'}"])

    min_item_level = filter_config.get("min_item_level")
    if min_item_level is not None:
        if item.item_level is None or item.item_level < int(min_item_level):
            return FilterResult(False, [f"item_level below minimum {min_item_level}"])
        reasons.append(f"item_level >= {min_item_level}")

    include_mods = filter_config.get("include_mods", [])
    searchable = "\n".join(item.explicit_mods + item.implicit_mods).lower()
    for phrase in include_mods:
        if phrase.lower() not in searchable:
            return FilterResult(False, [f"missing required mod phrase: {phrase}"])
        reasons.append(f"contains '{phrase}'")

    exclude_mods = filter_config.get("exclude_mods", [])
    for phrase in exclude_mods:
        if phrase.lower() in searchable:
            return FilterResult(False, [f"contains blocked mod phrase: {phrase}"])

    stat_thresholds = filter_config.get("stat_thresholds", {})
    for stat_name, threshold in stat_thresholds.items():
        item_value = item.stats.get(stat_name)
        if item_value is None:
            return FilterResult(False, [f"missing stat: {stat_name}"])
        if item_value < float(threshold):
            return FilterResult(False, [f"{stat_name} below threshold ({item_value} < {threshold})"])
        reasons.append(f"{stat_name} >= {threshold}")

    return FilterResult(True, reasons or ["matched default filter (no constraints)"])
