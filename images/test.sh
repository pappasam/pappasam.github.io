#!/bin/bash

convert_image() {
  convert sam-headshot-kepler-300x300.jpg -resize $1x$1 sam-headshot-kepler-$1x$1.png
}
