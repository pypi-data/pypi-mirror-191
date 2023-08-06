from typing import List, Optional

from .constants import REGEX_PATTERN_WORDS
from .numeral_converter import (
    NUMERAL_TREE,
    NumberItem,
    check_numeral_data_load,
    number_items2int,
    preprocess_numeral,
)


def convert_numerical_in_text(
    text: str,
    lang: str,
    max_corrections: Optional[int] = 0,
    max_corrections_relative: Optional[float] = None,
) -> str:
    """
    Converts numerical string in text into integer values

    :param str text: input text
    :param str lang: input text language
    :param int max_corrections: default value of maximum number of corrections
           in the query key when searching for a matching dictionary key;
           default = 2
    :param Optional[float] max_corrections_relative: default value to calculate
           maximum number of corrections in the query key when searching
           for a matching dictionary key; default = None
           calculated as round(max_corrections_relative * token_length)
    :return str: updated text with converted numerical into integer

    :Example:

    >>> s = "У цій школі працює шість психологів, "
    ...     "і кожен із нас має навантаження понад сто учнів"
    >>> convert_numerical_in_text(s, lang='uk')
    "У цій школі працює 6 психологів, і кожен із нас має навантаження понад 100 учнів"

    >>> s = "У моєму портфелі лежало чотири книги."
    >>> convert_numerical_in_text(s, lang='uk')
    "У моєму портфелі лежало 4 книги."

    """
    check_numeral_data_load(lang)

    updated_text = str()
    i = 0

    __number_items: List[NumberItem] = list()
    __prev_number_end = None  # type: Optional[int]

    for match in REGEX_PATTERN_WORDS.finditer(text):
        numeral = NUMERAL_TREE[lang].get(
            preprocess_numeral(match.group(), lang=lang),
            max_corrections=max_corrections,
            max_corrections_relative=max_corrections_relative,
        )

        if numeral:
            __number_item = NumberItem(
                numeral[0]["value"]["value"],
                numeral[0]["value"]["order"],
                numeral[0]["value"]["scale"],
            )

            # number starts
            if not len(__number_items):
                updated_text += text[i : match.span()[0]]
                __number_items.append(__number_item)
                __prev_number_end = match.span()[1]
                i = match.span()[1]

            # number continues
            elif match.span()[0] - __prev_number_end < 2:
                __number_items.append(__number_item)
                __prev_number_end = match.span()[1]
                i = match.span()[1]

            # prev number ends, new number starts
            else:
                updated_text += str(number_items2int(__number_items))
                updated_text += text[i : match.span()[0]]
                __number_items = [
                    __number_item,
                ]
                __prev_number_end = match.span()[1]
                i = match.span()[1]

    if __number_items:
        updated_text += str(number_items2int(__number_items))

    updated_text += text[i:]
    return updated_text
