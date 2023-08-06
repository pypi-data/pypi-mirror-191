# Numeral Converter

[![Coverage Status](https://img.shields.io/badge/%20Python%20Versions-%3E%3D3.9-informational)](https://pypi.org/project/numeral-converter/)
[![Coverage Status](https://coveralls.io/repos/github/SemioTricks/numeral-converter/badge.svg?branch=main)](https://coveralls.io/github/SemioTricks/numeral-converter?branch=main)

[![Coverage Status](https://img.shields.io/badge/Version-0.0.1-informational)](https://github.com/SemioTricks/numeral-converter)
[![Coverage Status](https://img.shields.io/badge/Docs-passed-green)](https://github.com/SemioTricks/numeral-converter/tree/main/docs)


Numeral converter:
- converts an integer value into a numerator in natural language, bringing it into the form given by the arguments
- converts the numerator from natural language to integer value
- 
- handles spelling errors


# Installation

> pip install numeral-converter

# Quickstart

## Loading Language Data

```python
from numeral_converter import (
    get_available_languages, 
    load_numeral_data,
    maximum_number_order_to_convert
)
get_available_languages()
# ['uk', 'ru', 'en']

load_numeral_data('en')
maximum_number_order_to_convert("en")
# 24

load_numeral_data('uk')
maximum_number_order_to_convert("uk")
# 33

load_numeral_data('ru')
maximum_number_order_to_convert("ru")
# 123
```

## Converting from Numeral to Integer

```python
from numeral_converter import numeral2int

numeral2int("two thousand and twenty-three", lang='en')
# 2023

numeral2int("дві тисячі двадцять третій", lang="uk")
# 2023

numeral2int("двох тисяч двадцяти трьох", lang="uk")
# 2023

numeral2int("двe тысячи двадцать третий", lang="ru")
# 2023

numeral2int("сто тисяч мільйонів", lang="uk")
# 100000000000

numeral2int("сто тисяч", lang="uk")
# 100000

numeral2int("три десятки", lang="uk")
# 30

numeral2int("три тисячі три сотні три десятки три", lang="uk")
# 3333
```

## Converting from Numeral to Integer (with mistakes)
```python
from numeral_converter import numeral2int

numeral2int("дви тисичи двадцить тре", lang="uk")
# 2023

numeral2int("дві тисячі двадцять три роки", lang="uk")
# ValueError('can\'t convert "роки" to integer')
        
numeral2int("три мільярди тисяча пятдесят пять мільонів", lang="uk")
# ValueError(
#     "position 1: order of 1000000000:9 is less/equal "
#     "of summary order in next group: 9")

numeral2int("три мільярди тисячний пятдесят пятий мільон", lang="uk")
# ValueError("the number in the middle of the numeral cannot be ordinal")
```

## Converting from Integer to Numeral
    
```python
from numeral_converter import int2numeral

int2numeral(2023, lang='uk', case="nominative", num_class="quantitative")
# {
#   'numeral': 'дві тисячі двадцять три', 
#   'numeral_forms': ['дві тисячі двадцять три', ]
# }

int2numeral(
    2021, 
    lang='uk',
    case="nominative",
    gender="neuter",
    num_class="quantitative")
# {
#   'numeral': 'дві тисячі двадцять одне (одно)', 
#   'numeral_forms': [
#       'дві тисячі двадцять одне',
#       'дві тисячі двадцять одно'
#    ]
# } 

int2numeral(
    89, 
    lang='uk',
    case="prepositional", 
    num_class="quantitative")
# {
#   'numeral': 'вісімдесяти (вісімдесятьох) дев’яти (дев’ятьох)', 
#   'numeral_forms': [
#       'вісімдесяти дев’яти',
#       'вісімдесяти дев’ятьох',
#       'вісімдесятьох дев’яти',
#       'вісімдесятьох дев’ятьох'
#    ]
# }    

int2numeral(10000000, lang="uk")
# {'numeral': 'десять мільйонів', 'numeral_forms': ['десять мільйонів']}
```

## Converting Numeral to Integer in Text
```python
from numeral_converter import convert_numerical_in_text
s = "After twenty, numbers such as twenty-five, fifty, seventy-five, " \
    "and one hundred follow. So long as one knows the core number, or the number " \
    "situated in the tens or hundreds position that determines the general " \
    "amount, understanding these more complicated numbers won't be difficult. " \
    "For example thirty-three is simply \"thirty\" plus three; sixty-seven " \
    "is \"sixty\" plus seven; and sixty-nine is simply \"sixty\" plus nine." \
convert_numerical_in_text(s, lang="en")
# "After 20, numbers such as 25, 50, 75, and 100 follow. So long as 1 "
# "knows the core number, or the number situated in the 10 or 100 "
# "position that determines the general amount, understanding these more "
# "complicated numbers won't be difficult. For example 33 is simply "
# "\"30\" plus 3; 67 is \"60\" plus 7; and 69 is simply \"60\" plus 9."
```