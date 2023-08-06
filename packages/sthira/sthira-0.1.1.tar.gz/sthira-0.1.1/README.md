# Sthira

> The word for "constant" in Sanskrit can be translated as "स्थिर" (sthira)


The `Constant` class is a metaclass for creating classes with constant attributes. 
Once set, the attributes of a `Constant` class cannot be changed, and new attributes cannot be added. 
This allows for creating classes that represent unchangeable values, such as constants, enums, and similar constructs. 
The Constant class also provides a `__str__`and `__repr__` implementation for convenient representation of the class.

# Installtion

`pip install sthira`

## Usage

```python
from sthira import constant


@constant
class Mammal:
    HUMAN = "human"
    TIGER = "tiger"
    LION = "lion"

@constant
class Bird:
    CROW = "crow"
    HAWK = "hawk"

@constant
class Fish:
    TUNA = "tuna"

@constant
class Animal:
    MAMMAL = Mammal
    BIRD = Bird
    FISH = Fish

print(f"{Animal.MAMMAL}")
print(f"{Animal.MAMMAL.HUMAN}")
print(f"{Animal.BIRD.CROW}")

```

> Output

```
Mammal
human
crow
```

## Cannot modify attributes

```python
Animal.MAMMAL.HUMAN = "HomoSapiens"

#     raise AttributeError("Cannot set or change the class attributes")
# AttributeError: Cannot set or change the class attributes
```

## Dispatch

> check `test_constant.py`

```python
from sthira import dispatch

@constant
class Red:
    BRICK = "#AA4A44"
    CADMIUM = "##D22B2B"


@constant
class Green:
    LIME = "#32CD32"
    LIGHT = "#90EE90"


@constant
class Color:
    RED = Red
    GREEN = Green
    YELLOW = "not_there_yet"

@dispatch
def get_color(color, input_):
	# Default implementation
	raise NotImplementedError("Unsupported color!")

@get_color.register(Color.RED)
def _(input_):
	return "I'm red"

@get_color.register(Color.GREEN)
def _(input_):
	return "hulk out!"

print(get_color(Color.GREEN, "input"))
# hulk out!
```


## Unit tests

```python -m unittest test_constant.py```

