import re
from collections import OrderedDict
from typing import Any, Dict

DEFAULT_MORPH: Dict[str, Any] = OrderedDict(
    [
        ("case", "nominative"),
        ("num_class", "cardinal"),
        ("number", "singular"),
        ("gender", "masculine"),
    ]
)

MORPH_FORMS: Dict[str, Any] = {
    "case": (
        "accusative",
        "dative",
        "genetive",
        "instrumental",
        "nominative",
        "prepositional",
    ),
    "num_class": (
        "cardinal",  # en: one, two, three etc.
        "collective",  # en: pair, dozen; uk: двое, троє, сотня
        "ordinal",  # en: first, second, third, etc.
    ),
    "gender": ("feminine", "masculine", "neuter"),
    "number": ("plural", "singular"),
}


REGEX_PATTERN_WORDS = re.compile("[a-zA-Zа-яА-ЯїЇґҐєЄёЁіІ'’]+")
