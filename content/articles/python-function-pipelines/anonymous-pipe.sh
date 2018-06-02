#!/bin/bash

# Count the number of words
echo "hello hello hello world world" | wc -w

# Count the number of words that are not "hello"
echo "hello hello hello world world" | sed 's/hello//g' | wc -w

# Count the number of words that are not "world"
echo "hello hello hello world world" | sed 's/world//g' | wc -w

# Should print the following to console:
# 5
# 2
# 3
