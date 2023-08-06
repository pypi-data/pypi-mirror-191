import warnings
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import semiotic_tricks_data_loader as stdl
from fuzzy_multi_dict import FuzzyMultiDict

from .constants import DEFAULT_MORPH

__NAME_ENV_STDL = "numeral_converter"
NUMERAL_TREE: Dict[str, Any] = dict()
NUMERAL_DATA: Dict[str, pd.DataFrame] = dict()


def get_available_languages() -> List[str]:
    """
    Check available languages

    :return List[str]: list of available languages identifier

    :Example:

    >>> from numeral_converter import get_available_languages
    >>> get_available_languages()
    ['uk', 'ru', 'en']

    """
    files, _ = stdl.DataLoader(is_delete_folder_with_same_name=True).get_paths(
        [__NAME_ENV_STDL]
    )

    return [file.split(".")[0] for file in files]


def load_numeral_data(lang: str):
    """
    Loads language `lang` data

    :param lang: language identifier;
           to find out the list of available languages, use `get_available_languages()`

    :Example:

    >>> from numeral_converter import load_numeral_data
    >>> load_numeral_data('uk')

    """
    if __is_loaded(lang):
        warnings.warn(f"data for language {lang} already load", UserWarning)
        return

    if not __is_available(lang):
        raise ValueError(
            f"no data for language {lang}; "
            f"use one of the available languages: {get_available_languages()}"
        )

    filename = stdl.DataLoader(is_delete_folder_with_same_name=True).load_file(
        [__NAME_ENV_STDL, f"{lang}.csv"]
    )

    NUMERAL_DATA[lang] = __read_language_data(filename)
    NUMERAL_TREE[lang] = __build_numeral_tree(NUMERAL_DATA[lang])


def maximum_number_order_to_convert(lang: str) -> int:
    """
    Order (log10(n)) of the maximum number that can be converted by the module
    for a given language

    :param lang: language identifier;
           to find out the list of available languages, use `get_available_languages()`
    :return int: max order

    :Example:
    >>> from numeral_converter import maximum_number_order_to_convert

    >>> maximum_number_order_to_convert('uk'))
    33

    >>>  maximum_number_order_to_convert('ru')
    123

    >>> maximum_number_order_to_convert('en')
    24

    """
    check_numeral_data_load(lang)
    return max(NUMERAL_DATA[lang]["order"].values)


def check_numeral_data_load(lang):
    if not __is_loaded(lang):
        warnings.warn(
            f'data for language "{lang}" is not loaded;'
            f'starts searching for data for language "{lang}"',
            UserWarning,
        )
        load_numeral_data(lang)


def __read_language_data(filename: Path) -> pd.DataFrame:
    df = pd.read_csv(filename, sep=",")
    df["order"] = df.order.apply(int)
    df["value"] = df.apply(
        lambda row: int(row.value) if row.order < 6 else None, axis=1
    )

    for c in df.columns:
        df[c] = df[c].apply(lambda x: None if pd.isnull(x) else x)

    return df


def __build_numeral_tree(df: pd.DataFrame) -> FuzzyMultiDict:
    numeral_tree = FuzzyMultiDict(update_value_func=__update_numeral_word_value)

    for i, row in df.iterrows():
        for string in row["string"].split(" "):
            if not string:
                continue

            data = {
                "morph_forms": {
                    label: row[label]
                    for label in DEFAULT_MORPH.keys()
                    if row.get(label) is not None
                },
                "value": row["value"] if row.order < 6 else 10**row.order,
                "order": row["order"],
                "scale": row["scale"],
            }

            numeral_tree[string] = data

    return numeral_tree


def __is_loaded(lang: str):
    return not (NUMERAL_TREE.get(lang) is None or NUMERAL_DATA.get(lang) is None)


def __is_available(lang: str) -> bool:
    __available_languages = get_available_languages()
    return lang in __available_languages


def __update_numeral_word_value(x, y):
    if x is None:
        return y

    if not isinstance(x, dict) or not isinstance(y, dict):
        raise TypeError(f"Invalid value type; expect dict; got {type(x)} and {type(y)}")

    for k, v in y.items():
        if x.get(k) is None:
            x[k] = v
        elif isinstance(x[k], list):
            x[k].append(v)
        elif x[k] != v:
            x[k] = [x[k], v]

    return x
