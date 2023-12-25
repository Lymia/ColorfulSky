#!/bin/sh
ls exported/all_data/*/loot_tables | grep -v "^blocks$" | grep -v "^entities$" | tr '\n' '~' | sed "s/~~/|/g" | tr '|' '\n' | grep -v ":$" | tr '~' '  '
