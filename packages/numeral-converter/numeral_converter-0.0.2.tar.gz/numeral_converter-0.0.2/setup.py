# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numeral_converter']

package_data = \
{'': ['*']}

install_requires = \
['fuzzy-multi-dict>=0.0.4,<0.0.5',
 'pandas>=1.5.3,<2.0.0',
 'semiotic-tricks-data-loader>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'numeral-converter',
    'version': '0.0.2',
    'description': '',
    'long_description': '# Numeral Converter\n\n[![Coverage Status](https://img.shields.io/badge/%20Python%20Versions-%3E%3D3.9-informational)](https://pypi.org/project/numeral-converter/)\n[![Coverage Status](https://coveralls.io/repos/github/SemioTricks/numeral-converter/badge.svg?branch=main)](https://coveralls.io/github/SemioTricks/numeral-converter?branch=main)\n\n[![Coverage Status](https://img.shields.io/badge/Version-0.0.1-informational)](https://github.com/SemioTricks/numeral-converter)\n[![Coverage Status](https://img.shields.io/badge/Docs-passed-green)](https://github.com/SemioTricks/numeral-converter/tree/main/docs)\n\n\nNumeral converter:\n- converts an integer value into a numerator in natural language, bringing it into the form given by the arguments\n- converts the numerator from natural language to integer value\n- \n- handles spelling errors\n\n\n# Installation\n\n> pip install numeral-converter\n\n# Quickstart\n\n## Loading Language Data\n\n```python\nfrom numeral_converter import (\n    get_available_languages, \n    load_numeral_data,\n    maximum_number_order_to_convert\n)\nget_available_languages()\n# [\'uk\', \'ru\', \'en\']\n\nload_numeral_data(\'en\')\nmaximum_number_order_to_convert("en")\n# 24\n\nload_numeral_data(\'uk\')\nmaximum_number_order_to_convert("uk")\n# 33\n\nload_numeral_data(\'ru\')\nmaximum_number_order_to_convert("ru")\n# 123\n```\n\n## Converting from Numeral to Integer\n\n```python\nfrom numeral_converter import numeral2int\n\nnumeral2int("two thousand and twenty-three", lang=\'en\')\n# 2023\n\nnumeral2int("дві тисячі двадцять третій", lang="uk")\n# 2023\n\nnumeral2int("двох тисяч двадцяти трьох", lang="uk")\n# 2023\n\nnumeral2int("двe тысячи двадцать третий", lang="ru")\n# 2023\n\nnumeral2int("сто тисяч мільйонів", lang="uk")\n# 100000000000\n\nnumeral2int("сто тисяч", lang="uk")\n# 100000\n\nnumeral2int("три десятки", lang="uk")\n# 30\n\nnumeral2int("три тисячі три сотні три десятки три", lang="uk")\n# 3333\n```\n\n## Converting from Numeral to Integer (with mistakes)\n```python\nfrom numeral_converter import numeral2int\n\nnumeral2int("дви тисичи двадцить тре", lang="uk")\n# 2023\n\nnumeral2int("дві тисячі двадцять три роки", lang="uk")\n# ValueError(\'can\\\'t convert "роки" to integer\')\n        \nnumeral2int("три мільярди тисяча пятдесят пять мільонів", lang="uk")\n# ValueError(\n#     "position 1: order of 1000000000:9 is less/equal "\n#     "of summary order in next group: 9")\n\nnumeral2int("три мільярди тисячний пятдесят пятий мільон", lang="uk")\n# ValueError("the number in the middle of the numeral cannot be ordinal")\n```\n\n## Converting from Integer to Numeral\n    \n```python\nfrom numeral_converter import int2numeral\n\nint2numeral(2023, lang=\'uk\', case="nominative", num_class="quantitative")\n# {\n#   \'numeral\': \'дві тисячі двадцять три\', \n#   \'numeral_forms\': [\'дві тисячі двадцять три\', ]\n# }\n\nint2numeral(\n    2021, \n    lang=\'uk\',\n    case="nominative",\n    gender="neuter",\n    num_class="quantitative")\n# {\n#   \'numeral\': \'дві тисячі двадцять одне (одно)\', \n#   \'numeral_forms\': [\n#       \'дві тисячі двадцять одне\',\n#       \'дві тисячі двадцять одно\'\n#    ]\n# } \n\nint2numeral(\n    89, \n    lang=\'uk\',\n    case="prepositional", \n    num_class="quantitative")\n# {\n#   \'numeral\': \'вісімдесяти (вісімдесятьох) дев’яти (дев’ятьох)\', \n#   \'numeral_forms\': [\n#       \'вісімдесяти дев’яти\',\n#       \'вісімдесяти дев’ятьох\',\n#       \'вісімдесятьох дев’яти\',\n#       \'вісімдесятьох дев’ятьох\'\n#    ]\n# }    \n\nint2numeral(10000000, lang="uk")\n# {\'numeral\': \'десять мільйонів\', \'numeral_forms\': [\'десять мільйонів\']}\n```\n\n## Converting Numeral to Integer in Text\n```python\nfrom numeral_converter import convert_numerical_in_text\ns = "After twenty, numbers such as twenty-five, fifty, seventy-five, " \\\n    "and one hundred follow. So long as one knows the core number, or the number " \\\n    "situated in the tens or hundreds position that determines the general " \\\n    "amount, understanding these more complicated numbers won\'t be difficult. " \\\n    "For example thirty-three is simply \\"thirty\\" plus three; sixty-seven " \\\n    "is \\"sixty\\" plus seven; and sixty-nine is simply \\"sixty\\" plus nine." \\\nconvert_numerical_in_text(s, lang="en")\n# "After 20, numbers such as 25, 50, 75, and 100 follow. So long as 1 "\n# "knows the core number, or the number situated in the 10 or 100 "\n# "position that determines the general amount, understanding these more "\n# "complicated numbers won\'t be difficult. For example 33 is simply "\n# "\\"30\\" plus 3; 67 is \\"60\\" plus 7; and 69 is simply \\"60\\" plus 9."\n```',
    'author': 'Tetiana Lytvynenko',
    'author_email': 'lytvynenkotv@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
