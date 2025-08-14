# Introduction
This doc is meant to track my conversations with VsCode's Copilot feature. I use this AI to answer questions that I may have and it helps me learn along the way.

## Table of contents
- [Why would I use pydantic in my Item class when I can just put name: str, price: float, etc without it?](#why-use-pydantic)
- [What does typing.union do? In reference to Union[str, None] = None?](#what-does-typing-union-do)
- [What is the enum library in Python?](#what-is-the-enum-library-in-python)
- [Explain this line of code for me: async def read_items(q: str | None = None):](#explain-this-line-of-code-for-me-async-def-read_itemsq-str--none--none)

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