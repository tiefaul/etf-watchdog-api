# Introduction
This doc is meant to track my conversations with VsCode's Copilot feature. I use this AI to answer questions that I may have and it helps me learn along the way.

## Table of contents
- [Why would I use pydantic in my Item class when I can just put name: str, price: float, etc without it?](#why-use-pydantic)
- [What does typing.union do? In reference to Union[str, None] = None?](#what-does-typing-union-do)

---

## Questions for Copilot
### Why would I use pydantic in my Item class when I can just put name: str, price: float, etc without it?

- You use Pydantic's BaseModel (as in your Item class) to get automatic data validation, parsing, and serialization/deserialization for your API endpoints. Pydantic will attempt to coerce compatible types. If you submit a string like "3.14" for a field declared as price: float, Pydantic will convert it to a float (3.14).

### what does typing.union do? In reference to Union[str, None] = None?

- typing.Union allows you to specify that a variable or parameter can be more than one type. In your example, Union[str, None] means the value can be either a string or None (i.e., it’s optional). = None means that the parameter or attribute defaults to None if no value is provided.