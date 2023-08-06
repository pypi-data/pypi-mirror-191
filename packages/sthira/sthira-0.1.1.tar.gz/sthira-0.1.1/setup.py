# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sthira']
setup_kwargs = {
    'name': 'sthira',
    'version': '0.1.1',
    'description': 'The `Constant` class is a metaclass for creating classes with constant attributes',
    'long_description': '# Sthira\n\n> The word for "constant" in Sanskrit can be translated as "स्थिर" (sthira)\n\n\nThe `Constant` class is a metaclass for creating classes with constant attributes. \nOnce set, the attributes of a `Constant` class cannot be changed, and new attributes cannot be added. \nThis allows for creating classes that represent unchangeable values, such as constants, enums, and similar constructs. \nThe Constant class also provides a `__str__`and `__repr__` implementation for convenient representation of the class.\n\n# Installtion\n\n`pip install sthira`\n\n## Usage\n\n```python\nfrom sthira import constant\n\n\n@constant\nclass Mammal:\n    HUMAN = "human"\n    TIGER = "tiger"\n    LION = "lion"\n\n@constant\nclass Bird:\n    CROW = "crow"\n    HAWK = "hawk"\n\n@constant\nclass Fish:\n    TUNA = "tuna"\n\n@constant\nclass Animal:\n    MAMMAL = Mammal\n    BIRD = Bird\n    FISH = Fish\n\nprint(f"{Animal.MAMMAL}")\nprint(f"{Animal.MAMMAL.HUMAN}")\nprint(f"{Animal.BIRD.CROW}")\n\n```\n\n> Output\n\n```\nMammal\nhuman\ncrow\n```\n\n## Cannot modify attributes\n\n```python\nAnimal.MAMMAL.HUMAN = "HomoSapiens"\n\n#     raise AttributeError("Cannot set or change the class attributes")\n# AttributeError: Cannot set or change the class attributes\n```\n\n## Dispatch\n\n> check `test_constant.py`\n\n```python\nfrom sthira import dispatch\n\n@constant\nclass Red:\n    BRICK = "#AA4A44"\n    CADMIUM = "##D22B2B"\n\n\n@constant\nclass Green:\n    LIME = "#32CD32"\n    LIGHT = "#90EE90"\n\n\n@constant\nclass Color:\n    RED = Red\n    GREEN = Green\n    YELLOW = "not_there_yet"\n\n@dispatch\ndef get_color(color, input_):\n\t# Default implementation\n\traise NotImplementedError("Unsupported color!")\n\n@get_color.register(Color.RED)\ndef _(input_):\n\treturn "I\'m red"\n\n@get_color.register(Color.GREEN)\ndef _(input_):\n\treturn "hulk out!"\n\nprint(get_color(Color.GREEN, "input"))\n# hulk out!\n```\n\n\n## Unit tests\n\n```python -m unittest test_constant.py```\n\n',
    'author': 'neelabalan',
    'author_email': 'neelabalan.n@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
