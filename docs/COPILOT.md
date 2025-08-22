# Introduction

This doc is meant to track my conversations with VsCode's Copilot feature. I use this AI to answer questions that I may have and it helps me learn along the way. Think of it as a tutor, while you go through a course.

## Table of contents

- [Why would I use pydantic in my Item class when I can just put name: str, price: float, etc without it?](#why-use-pydantic)
- [What does typing.union do? In reference to Union[str, None] = None?](#what-does-typing-union-do)
- [What is the enum module in Python?](#what-is-the-enum-module-in-python)
- [Explain this line of code for me: async def read_items(q: str | None = None):](#explain-this-line-of-code-for-me-async-def-read_itemsq-str--none--none)
- [What does Annotated do in the typing library?](#what-does-annotated-do-in-the-typing-library)
- [Can I write != instead of is not? Example: `if item.tax != None`](#can-i-write--instead-of-is-not-example-if-itemtax--none)
- [Does the order of the default values matter?](#does-the-order-of-the-default-values-matter)

---

## Questions for Copilot
### Why would I use pydantic in my Item class when I can just put name: str, price: float, etc without it?

- You use Pydantic's BaseModel (as in your Item class) to get automatic data validation, parsing, and serialization/deserialization for your API endpoints. Pydantic will attempt to coerce compatible types. If you submit a string like "3.14" for a field declared as price: float, Pydantic will convert it to a float (3.14).

### what does typing.union do? In reference to Union[str, None] = None?

- typing.Union allows you to specify that a variable or parameter can be more than one type. In your example, Union[str, None] means the value can be either a string or None (i.e., it’s optional). = None means that the parameter or attribute defaults to None if no value is provided.

### What is the enum library in Python?

- An enum (short for "enumeration") is a special data type that defines a set of named, constant values. In Python, you use the Enum class from the enum module to create enums. Enums are useful for representing a fixed set of related options, such as days of the week, user roles, or status codes, making your code more readable and less error-prone. Example:

```python
from enum import Enum

class Day(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

# Usage:
today = Day.WEDNESDAY
print(today)           # Output: Day.WEDNESDAY
print(today.value)     # Output: 3
print(today.name)      # Output: 'WEDNESDAY'
```

### Explain this line of code for me: async def read_items(q: str | None = None):

- This line defines an asynchronous function named read_items with one optional parameter:
    - async def: Declares the function as asynchronous, allowing you to use await inside it for non-blocking operations (like database or network calls).
    - read_items: The function name.
    - q: str | None = None: The parameter q can be a string or None (optional). The default value is None, so if no argument is provided, q will be None.
- In summary, this function can be called with or without a string argument for q, and it can perform asynchronous operations.


### What does Annotated do in the typing library?

- On its own Annotated does not do anything other than assigning extra information (metadata) to a reference. It is up to another code, which can be a library, framework or your own code, to interpret the metadata and make use of it.

- For example, FastAPI uses Annotated for data validation:

``` python
def read_items(q: Annotated[str, Query(max_length=50)])
```

- Here the parameter q is of type str with a maximum length of 50. This information was communicated to FastAPI (or any other underlying library) using the Annotated keyword.

### Can I write != instead of is not? Example: `if item.tax != None`

- For most value comparisons in Python, you can use `!=` instead of `is not`, but for checking against None, it is best practice to use is not None rather than != None.
    - Use `is not None` for identity checks (recommended for None).
    - Use `!=` for value comparisons (e.g., numbers, strings).

- Some other identity checks include:
    - Checking if two variables refer to the exact same object:
    ```python
    if a is b:
    # a and b are the same object in memory
    ```
    - Checking if a variable is not a specific singleton (like `None`, `True`, or `False`)
    ```python
    if flag is True:
    # flag is exactly the singleton True
    if result is not False:
    # result is not the singleton False
    ```
    - Example of using !=
    ```python
    if x != "hello":
    # or
    if x != 2:
    ```

### Does the order of the default values matter?

- Yes, the order of default values matters in Python function definitions, including FastAPI endpoints.
- All parameters without default values (i.e., required parameters) must come before any parameters with default values (i.e., optional parameters). If you put a required parameter after an optional one, Python will raise a SyntaxError.
- For example, this is correct:
```python
def update_item(item_id: int, item: Item, q: str | None = None, user: User | None = None):
```
- But this will cause an error:
```python
def update_item(q: str | None = None, item: Item):  # ❌ Not allowed
```
- So, always list required parameters first, then optional ones with default values.