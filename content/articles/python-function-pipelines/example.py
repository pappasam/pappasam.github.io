#!/usr/bin/env python
'''Simple function example'''

# functions: begin
def add_5(value: int) -> int:
    return value + 5

def add_6(value: int) -> int:
    return value + 6

def add_7(value: int) -> int:
    return value + 7
# functions: end

# reassignment: begin
x_0 = 0
x_5 = add_5(x_0)
x_6 = add_6(x_5)
x = add_7(x_6)

print(f'x={x}')
# reassignment: end

# simple reduce: begin
from functools import reduce
y = reduce(
    lambda value, function: function(value),
    (
        add_5,
        add_6,
        add_7,
    ),
    0,
)

print(f'y={y}')
# simple reduce: end

# pipeline: begin
from typing import TypeVar, Callable, Sequence

T = TypeVar('T')

def pipeline(
        value: T,
        function_pipeline: Sequence[Callable[[T], T]],
) -> T:
    '''A generic Unix-like pipeline

    :param value: the value you want to pass through a pipeline
    :param function_pipeline: an ordered list of functions that
        comprise your pipeline
    '''
    return reduce(lambda v, f: f(v), function_pipeline, value)

z = pipeline(
    value=0,
    function_pipeline=(
        add_5,
        add_6,
        add_7,
    )
)

print(f'z={z}')
# pipeline: end
