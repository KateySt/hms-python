#!/bin/bash

read -p "Enter file name: " NAME

if [ -z "$NAME" ]; then
  echo "No file name provided"
  exit 1
fi

touch "$NAME"
echo "File '$NAME' created successfully"
