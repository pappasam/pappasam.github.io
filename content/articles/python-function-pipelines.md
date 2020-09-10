---
title: Python Function Pipelines
date: 2018-06-02
category: Software Development
modified: 2018-06-02
tags: Python, Unix, pipeline, functional programming
summary: Develop a simple, strongly-typed function pipeline for your personal projects to make beautiful, explicit, Unix-like pipelines in Python.
---

[TOC]

If your Python code represents a function pipeline, it should look like a function pipeline. This post presents a simple, strongly-typed function pipeline for your personal projects to make beautiful, explicit, Unix-like pipelines in Python.  Requires Python 3.6 or greater.

I was reading through the pytorch reinforcement learning [documentation](https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html) today and came across the following irksome pattern:

```python
{! ./python-function-pipelines/pytorch-reinforcement-learning.py !}
```

The manipulation and reassignment of a variable *x* to itself as it is passed through a neural network's gateways makes neural networks that much harder to follow. IMHO, explicit variable **reassignment** is almost always bad because it makes it hard for my limited human brain to track a variable name's associated data during program execution. If a program tells me that *x* is an integer on line 10 and then **reassigns** it to a string on line 20, I will want to delete said program from my computer, take a cold shower, and exact revenge on the program's author. With that established, let's just avoid reassignment altogether.

## The problem

In the above example, variable reassignment is convenient. It prevents the programmer from needing to come up with new names for each state in the connected pipeline. How can we find an elegant way of avoiding explicit variable reassignment in the pipeline use-case while still producing readable, performant code? The answer: take inspiration from Unix pipes!

## Unix pipes

In the Unix shell, virtually everything we work with has the same type: a [file](https://en.wikipedia.org/wiki/Everything_is_a_file). "Everything is a File" makes it easy to chain functions together because all commands take files as inputs and return files as outputs.  One common way to chain system calls in Unix is called the [anonymous pipe](https://en.wikipedia.org/wiki/Anonymous_pipe), which enables programmers to chain command line programs together to manipulate a text stream. See the following example:

```bash
{! ./python-function-pipelines/anonymous-pipe.sh !}
```

Notice that data flows **through** the pipeline and no variable reassignment is used. The Unix pipeline is beautiful in this regard; I'd like to build something similar in Python.

## Example

Let's say we have the following three functions:

```python
{! ./python-function-pipelines/example.py [ln:4-11] !}
```

Our **example problem**: take an initial integer 0 and add 5, then 6, then 7 to it using our three functions so that our final result is 18.

### Solution 1: name each step in the pipeline

We can do slightly better than the pytorch example and create a unique variable
name for each step in the process.

```python
{! ./python-function-pipelines/example.py [ln:13-18] !}
```

Besides being pretty ugly / hard to read, this creates some useless names in our module's scope. Do we really need to give each step its own name? We don't use the steps anywhere else and this makes the pipeline pretty hard to edit. This solution almost makes we wish we could go back to reassignment. Fortunately, the entire pipeline can be expressed with one name thanks to the "reduce" function.

### Solution 2: use the "reduce" function

```python
{! ./python-function-pipelines/example.py [ln:20-31] !}
```

This example uses the standard library "reduce" function. Originally, "reduce" was intended to take a list of values and collapse them into one value. This use-case is described well in the [Python documentation](https://docs.python.org/3/library/functools.html#functools.reduce) and in this [YouTube](https://www.youtube.com/watch?v=ZrZ6vJGiE8I) video. Here, we use it a bit differently. Instead of taking a list of values and applying a "collapsing" function to them, we take a list of functions and pass a value through them. This has obvious advantages over solution 1: we can easily swap new functions in and out of the pipeline to suit our needs without needing to adjust any other code / rename pipeline steps (because we haven't named the steps at all!).

This solution frees us from naming each step in our pipeline but it does have some disadvantages: "reduce" is kind of hard to read and this use-case isn't quite standard. Whenever we find ourselves using a standard library function in a confusing way, that's a signal that we should probably define our own function to make this clearer to ourselves and to those who read our code.

### Solution 3: custom "pipeline" function

```python
{! ./python-function-pipelines/example.py [ln:33-58] !}
```

This solution is elegant and explicit. It is generic and works with mypy. As long as our function pipeline contains only functions that take our value's type and return our value's type (similar to Unix command line utilities, where everything is a file), this pipeline will successfully pass our value in a type-safe way.

## Full script

```python
{! ./python-function-pipelines/example.py !}
```

## Conclusion

If your system resembles a pipeline, don't reassign your piped variable to itself. There is a better way and it's pretty much built into Python.  You'll just need to care enough to use it.
