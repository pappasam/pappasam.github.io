---
title: Immediate execution of Python class definitions
date: 2021-10-29
category: Software Development
modified: 2021-10-29
tags: python, class, function, module
summary: Classes are confusing. Python class definitions are especially confusing. Learn how the code execution environment differs between Python's "class definitions", "function bodies", and "modules".
---

<!-- markdownlint-disable MD033 -->

[TOC]

<!-- https://docs.python.org/3/tutorial/classes.html#classes -->
<!-- https://docs.python.org/3/tutorial/modules.html#modules -->
<!-- https://docs.python.org/3/tutorial/controlflow.html#defining-functions -->
<!-- https://docs.python.org/3/reference/import.html#packages -->

Code placed at the top-level of a Python [class definition](https://docs.python.org/3/tutorial/classes.html#classes) executes immediately, during "class creation" (which differs. This, at-times unexpectedly, resembles code placed at the [module level](https://docs.python.org/3/tutorial/modules.html#modules) and differs significantly from code living in Python [function bodies](https://docs.python.org/3/tutorial/controlflow.html#defining-functions).

This may not sound strange, but it can confuse heck out of beginners. In order to see this at work, we'll begin with the following simple example:

```python
class WillFail:
    raise ValueError("I have raised")
    def hello(self):
        return "world"
print("I will never be called :(")
```

If class statements behaved as most users expect, you'd think this would print `I will never be called :(` to the console. Sadly, that negative statement will never see the light of day...

```console
$ python main.py
Traceback (most recent call last):
  File "/path/to/main.py", line 1, in <module>
    class WillFail:
  File "/path/to/main.py", line 2, in WillFail
    raise ValueError("I have raised")
ValueError: I have raised
```

## First: modules

The first concept we'll cover are [modules]()

## Functions

This blog post was inspired by a persistent problem I've faced when using [SQLAlchemy](https://www.sqlalchemy.org/).
