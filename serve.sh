#!/bin/bash

find content/ | entr -sr 'make serve'
