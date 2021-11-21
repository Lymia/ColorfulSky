#!/bin/bash

rm -v data/forge/tags/items/ores/*
rm -v data/forge/tags/items/storage_blocks/*

cd data/forge/tags/items/ores
ln -sv ../../blocks/ores/* .

cd ../storage_blocks
ln -sv ../../blocks/storage_blocks/* .
