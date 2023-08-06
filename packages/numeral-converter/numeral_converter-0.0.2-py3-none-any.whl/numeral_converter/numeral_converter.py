import logging
import math
import re
import warnings
from collections import namedtuple
from typing import Any, Dict, List, Optional

from .constants import DEFAULT_MORPH, MORPH_FORMS
from .lang_data_loader import NUMERAL_DATA, NUMERAL_TREE, check_numeral_data_load
from .utils import combinations

NumberItem = namedtuple("NumberItem", "value order scale")
NumeralWord = namedtuple("NumeralWord", "default alt")


logger = logging.getLogger(__name__)


def numeral2int(numeral: str, lang: str) -> Optional[int]:
    """
    Converts input numeral in language `lang` into integer value

    To find out the order (log10(n)) of the maximum number that can be converted
    by the module use `maximum_number_order_to_convert()`

    :param numeral: input numeral in language `lang`
    :param lang: language identifier;
           to find out the list of available languages, use `get_available_languages()`
    :return Optional [int]: integer value; None if it fails to convert

    :Example:

    >>> from numeral_converter import load_numeral_data, numeral2int

    >>> load_numeral_data("uk")
    >>> numeral2int("сорок два", lang="uk")
    42

    >>> # different morph forms
    >>> numeral2int("сорок другий", lang="uk")
    42

    >>> # spell checking
    >>> numeral2int("сороак двоіх", lang="uk")
    42

    # another languages
    >>> load_numeral_data("ru")
    >>> numeral2int("сорок второй", lang="ru")
    42

    >>> load_numeral_data("en")
    >>> numeral2int("forty two", lang="en")
    42

    """
    number_items = numeral2number_items(numeral=numeral, lang=lang)
    value = number_items2int(number_items=number_items)
    return value


def int2numeral(value: int, lang: str, **kwargs):
    """
    Converts input integer number into a numeral in language `lang`
    into a morphological form given by the argument-parameters

    To find out the order (log10(n)) of the maximum number that can be converted
    by the module use `maximum_number_order_to_convert()`


    Possible argument-parameters and their possible values:

    - "case": nominative', 'genetive', 'dative', 'instrumental', 'accusative'
              or 'prepositional';
    - "num_class": 'ordinal', 'cardinal' or 'collective';
    - "gender": 'masculine', 'feminine' or 'neuter';
    - "number": 'plural' or 'singular'

    :param value: input integer value
    :param lang: language identifier;
           to find out the list of available languages, use `get_available_languages()`
    :return str: string numeral in language `lang` in a morphological form
            given by the argument-parameters

    :Example:

    >>> from numeral_converter import load_numeral_data, int2numeral
    >>> load_numeral_data("uk")

    >>> int2numeral(42, case="nominative", num_class="cardinal")
    {
        'numeral': 'сорок два',
        'numeral_forms': ['сорок два', ]
    }

    >>> int2numeral(42, lang='uk', case="nominative", num_class="cardinal")
    {'numeral': 'сорок два', 'numeral_forms': ['сорок два']}

    >>> int2numeral(42, lang='uk', case="genetive", num_class="cardinal")
    {'numeral': 'сорока двох', 'numeral_forms': ['сорока двох']}

    >>> int2numeral(
    ...     42, lang='uk', case="dative", num_class="ordinal", gender='feminine')
    {'numeral': 'сорок другій', 'numeral_forms': ['сорок другій']}

    """
    __check_kwargs(kwargs)

    numeral_items = int2number_items(value, lang)

    numeral = number_items2numeral(
        numeral_items,
        lang=lang,
        case=kwargs.get("case"),
        num_class=kwargs.get("num_class"),
        gender=kwargs.get("gender"),
        number=kwargs.get("number"),
    )

    return numeral


def numeral2number_items(numeral: str, lang: str):
    check_numeral_data_load(lang)
    numeral = preprocess_numeral(numeral, lang)

    number_items: List[NumberItem] = list()

    for i, number_word in enumerate(numeral.split(" ")[::-1]):
        number_word_info = NUMERAL_TREE[lang].get(number_word)
        if not len(number_word_info):
            raise ValueError(f'can\'t convert "{number_word}" to integer')

        if i > 0:
            number_word_info = __delete_ordinal_from_numeral_word_info(number_word_info)
            if not len(number_word_info):
                raise ValueError(f'ordinal numeral word "{number_word}" inside numeral')

        __item = number_word_info[0]["value"]
        number_items.insert(
            0,
            NumberItem(
                value=__item["value"] if not __item["scale"] else 10 ** __item["order"],
                order=__item["order"],
                scale=__item["scale"],
            ),
        )

    return number_items


def number_items2int(number_items: List[NumberItem]) -> int:
    int_value = 0
    number_items = number_items[::-1]

    i_number = num_block_start = 0
    num_block_order = 0

    if number_items[0].scale:
        i_number = num_block_start = 1
        num_block_order = number_items[0].order

    while i_number < len(number_items):
        i_number, inner_order = __search_block(number_items, i_number, num_block_order)
        __check_correct_order(number_items, num_block_start, i_number, inner_order)
        __value = (
            number_items2int(number_items[num_block_start:i_number][::-1])
            if inner_order
            else max(sum([x.value for x in number_items[num_block_start:i_number]]), 1)
        )

        int_value += (10**num_block_order) * __value
        if i_number >= len(number_items):
            return int(int_value)

        __check_number_is_correct_scale(number_items, i_number, int_value)
        num_block_order = number_items[i_number].order
        num_block_start = i_number + 1
        i_number += 1

    if num_block_start is not None:
        int_value += 10**num_block_order

    return int(int_value)


def int2number_items(number: int, lang: str) -> List[NumberItem]:
    check_numeral_data_load(lang)
    if number == 0:
        return [
            NumberItem(0, -1, None),
        ]

    number_items: List[NumberItem] = list()
    current_order, ones = 0, None  # type: int, Optional[int]

    mem = None

    while number:
        digit = number % 10
        if current_order % 3 == 2 and digit:
            if mem:
                number_items.insert(0, mem)
                mem = None
            number_items.insert(0, NumberItem(100 * digit, current_order % 3, None))

        elif current_order % 3 == 0:
            ones = digit
            if current_order > 0:
                mem = NumberItem(10**current_order, current_order, True)
        else:
            if digit == 1 and ones > 0:
                value = 10 * digit + ones
                if value:
                    if mem:
                        number_items.insert(0, mem)
                        mem = None
                    number_items.insert(0, NumberItem(value, current_order % 3, None))
            else:
                if ones:
                    if mem:
                        number_items.insert(0, mem)
                        mem = None
                    number_items.insert(0, NumberItem(ones, 0, None))

                if digit:
                    if mem:
                        number_items.insert(0, mem)
                        mem = None
                    number_items.insert(
                        0, NumberItem(10 * digit, current_order % 3, None)
                    )

            ones = None

        current_order += 1
        number = number // 10

    if ones:
        if mem:
            number_items.insert(0, mem)
        number_items.insert(0, NumberItem(ones, 0, None))

    if number_items[0].scale is not None:
        number_items.insert(0, NumberItem(1, 0, None))
    elif number_items[0].value == 100 and lang == "en":
        number_item = NumberItem(number_items[0].value, number_items[0].order, True)
        number_items = number_items[1:]
        number_items.insert(0, number_item)
        number_items.insert(0, NumberItem(1, 0, None))

    return number_items


def int2numeral_word(value: int, lang: str, **kwargs) -> NumeralWord:
    __check_kwargs(kwargs)
    check_numeral_data_load(lang)

    if value == 0 or math.log10(value) < 6:
        sub_data = NUMERAL_DATA[lang][NUMERAL_DATA[lang].value == value]
    else:
        sub_data = NUMERAL_DATA[lang][
            NUMERAL_DATA[lang].order == int(math.log10(value))
        ]

    if sub_data.shape[0] == 0:
        raise ValueError(f"no data for number {value}")

    for label, default in DEFAULT_MORPH.items():
        label_value = kwargs.get(label) or default
        if label_value and label not in NUMERAL_DATA[lang].columns:
            warnings.warn(
                f'no column "{label}" in data for language "{lang}"; ignored',
                UserWarning,
            )

        if label_value and label in sub_data.columns:
            if label_value in sub_data[label].values:
                sub_data = sub_data[sub_data[label] == label_value]
            elif kwargs.get(label):
                warnings.warn(
                    f"no data for {label} == {kwargs.get(label)}; ignored", UserWarning
                )
    if sub_data.shape[0] != 1:
        val_info = __kwargs2str(value=value, kwargs=kwargs)
        if sub_data.shape[0] == 0:
            raise ValueError(f"No data for {val_info}")
        if sub_data.shape[0] > 1:
            raise ValueError(
                f"There are more then one values for {val_info}:\n" f"{sub_data.head()}"
            )

    numeral_words = [x.strip() for x in sub_data.iloc[0].string.split(" ") if x]
    return NumeralWord(numeral_words[0], numeral_words[1:])


def number_items2numeral(number_items: List[NumberItem], lang: str, **kwargs):
    mf = {label: kwargs.get(label) or value for label, value in DEFAULT_MORPH.items()}
    if mf["num_class"] == "collective" and len(number_items) > 1:
        warnings.warn("Can't convert to collective numeral number; cardinal used")
        mf["num_class"] = "cardinal"

    numbers = list()
    for i, number_item in enumerate(number_items):
        if i == len(number_items) - 1:
            case = __define_morph_case(mf["case"], number_items, i, mf["num_class"])
            number = __define_morph_number(mf["number"], number_items, i)
            numbers.append(
                int2numeral_word(
                    number_item.value,
                    lang=lang,
                    case=case,
                    number=number,
                    num_class=mf["num_class"],
                    gender=mf["gender"],
                )
            )
            continue

        if (
            (0 < number_item.value < 10)
            and (i + 1 < len(number_items))
            and number_items[i + 1].scale
        ):
            gender = __define_morph_gender(number_items, i)
            case = __define_morph_case(mf["case"], number_items, i, mf["num_class"])
            numbers.append(
                int2numeral_word(number_item.value, lang=lang, case=case, gender=gender)
            )
            continue

        if number_item.scale:
            case = __define_morph_case(mf["case"], number_items, i, mf["num_class"])
            number = __define_morph_number(mf["number"], number_items, i)
            numbers.append(
                int2numeral_word(number_item.value, lang=lang, case=case, number=number)
            )
            continue

        case = __define_morph_case(mf["case"], number_items, i, mf["num_class"])
        numbers.append(int2numeral_word(number_item.value, lang=lang, case=case))

    return __process_numbers(numbers, number_items, lang=lang)


def __check_kwargs(kwargs):
    for label, label_item in kwargs.items():
        if MORPH_FORMS.get(label) is None:
            raise ValueError(f"Invalid label; use one of {MORPH_FORMS.keys()}")
        if label_item and label_item not in MORPH_FORMS[label]:
            raise ValueError(
                f"Invalid label {label} value; use one of {MORPH_FORMS[label]}"
            )


def __process_numbers(
    numbers: List[NumeralWord], number_items, lang: str
) -> Dict[str, Any]:
    if lang == "en":
        numbers__ = numbers.copy()
        numbers = list()
        i = 0
        while i < len(number_items):
            if (
                i + 1 < len(number_items)
                and number_items[i].order == 1
                and number_items[i + 1].order == 0
            ):
                numbers.append(
                    NumeralWord(
                        numbers__[i].default + "-" + numbers__[i + 1].default, []
                    )
                )
                i += 2
            else:
                numbers.append(numbers__[i])
                i += 1

    numeral = " ".join(
        [
            f"{number.default}" + (f" ({', '.join(number.alt)})" if number.alt else "")
            for number in numbers
        ]
    )

    numeral_forms = [
        " ".join(
            [
                (
                    [
                        numbers[i].default,
                    ]
                    + numbers[i].alt
                )[j]
                for i, j in enumerate(__combinations)
            ]
        )
        for __combinations in combinations(
            *[range(1 + len(number.alt)) for number in numbers]
        )
    ]

    return {"numeral": numeral, "numeral_forms": numeral_forms}


def preprocess_numeral(numeral: str, lang: str) -> str:
    if lang == "en":
        numeral = re.sub(r"-", " ", numeral)
        numeral = re.sub(r"\sand\s", " ", numeral)

    numeral = re.sub(r"\s+", " ", numeral).strip()

    numeral = numeral.lower()

    return numeral


def __delete_ordinal_from_numeral_word_info(
    number_word_info: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    return [
        item
        for item in number_word_info
        if (
            not isinstance(item["value"]["morph_forms"], list)
            and item["value"]["morph_forms"].get("num_class") != "ordinal"
        )
        or all(
            [
                (v.get("num_class") is None or v.get("num_class") != "ordinal")
                for v in item["value"]["morph_forms"]
            ]
        )
    ]


def __check_correct_order(
    number_items: List[NumberItem], start: int, end: int, inner_order: Optional[int]
):
    for k in range(start + 1, end):
        __order = (
            0
            if number_items[k].value % 10 ** number_items[k].order
            else number_items[k].order
        )

        if not inner_order and number_items[k - 1].order >= __order:
            raise ValueError(
                f"position {len(number_items) - k}: {number_items[k - 1].value}"
                f" with order {number_items[k - 1].order} stands after "
                f"{number_items[k].value} with less/equal order {__order}"
            )

        if inner_order and number_items[k - 1].order == __order:
            raise ValueError(
                f"position {len(number_items) - k}: {number_items[k - 1].value}"
                f" with order {number_items[k - 1].order} stands after "
                f"{number_items[k].value} with equal order {__order}"
            )


def __search_block(number_items, start, num_block_order):
    inner_order = None
    while start < len(number_items) and (
        not number_items[start].scale or number_items[start].order < num_block_order
    ):
        if number_items[start].scale and (
            inner_order is None or inner_order < number_items[start].order
        ):
            inner_order = number_items[start].order
        start += 1
    return start, inner_order


def __check_number_is_correct_scale(number_items, i_number, int_value):
    if not number_items[i_number].scale:
        raise ValueError(
            f"position {len(number_items) - 1 - i_number}: expects 10^(3n) or 100; "
            f"found {number_items[i_number].value}"
        )

    value_order = int(math.log10(int_value))
    if number_items[i_number].order <= value_order:
        raise ValueError(
            f"position {len(number_items) - 1 - i_number}: order of "
            f"{number_items[i_number].value}:{number_items[i_number].order} "
            f"is less/equal of summary order in next group: {value_order}"
        )


def __kwargs2str(value, kwargs):
    labels_string = ", ".join(
        [
            f'{label} = "{kwargs.get(label) or default}"'
            for label, default in DEFAULT_MORPH.items()
            if (kwargs.get(label) or default)
        ]
    )
    return f"number {value} ({labels_string})"


def __define_morph_number(
    global_number: str, number_items: List[NumberItem], i: int
) -> str:
    number = global_number

    prev_value = number_items[i - 1].value if i > 0 else 1

    if number_items[i].scale:
        number = "singular" if prev_value == 1 else "plural"

    return number


def __define_morph_case(global_case, number_items, i, global_num_class):
    case = global_case
    prev_value = number_items[i - 1].value if i > 0 else 1

    if i == len(number_items) - 1:
        if number_items[i].scale:
            case = (
                "nominative"
                if prev_value == 1
                else "nominative"
                if prev_value in (2, 3, 4)
                else "genetive"
            )

        return case

    if global_num_class == "ordinal":
        case = "nominative"

    if (
        (0 < number_items[i].value < 10)
        and (i + 1 < len(number_items))
        and number_items[i + 1].scale
    ):
        if case == "accusative":
            case = "nominative"
        return case

    if number_items[i].scale:
        if case in ("nominative", "accusative"):
            case = "nominative" if prev_value in (1, 2, 3, 4) else "genetive"
            return case

    if case == "accusative" and i != len(number_items) - 2:
        case = "nominative"

    return case


def __define_morph_gender(number_items, i):
    return "feminine" if number_items[i + 1].value == 1000 else "masculine"
