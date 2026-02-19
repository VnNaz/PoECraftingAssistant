from poe2_assistant.filters import evaluate_filter
from poe2_assistant.parser import parse_item_text


SAMPLE_ITEM = """Item Class: Quarterstaves
Rarity: Rare
Doom Reed
Ironwood Quarterstaff
--------
Item Level: 78
--------
+95 to Maximum Life
+34% to Fire Resistance
18% increased Physical Damage
"""


def test_filter_hit():
    item = parse_item_text(SAMPLE_ITEM)
    result = evaluate_filter(
        item,
        {
            "rarity": "Rare",
            "item_class": "Quarterstaves",
            "min_item_level": 75,
            "include_mods": ["Maximum Life"],
            "stat_thresholds": {"to_maximum_life": 90},
        },
    )

    assert result.matched is True


def test_filter_miss_on_excluded_mod():
    item = parse_item_text(SAMPLE_ITEM)
    result = evaluate_filter(
        item,
        {
            "exclude_mods": ["increased Physical Damage"],
        },
    )

    assert result.matched is False
