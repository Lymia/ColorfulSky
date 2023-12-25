#!/bin/bash

cd docs/exported || exit 1

rm -rfv all_assets all_data tmp || exit 1
mkdir tmp || exit 1

cd tmp || exit 1
    for i in ../../../../mods/*.jar; do
        unzip -b -D -o "$i" || exit 1
    done
cd .. || exit 1

mv -v tmp/assets all_assets || exit 1
mv -v tmp/data all_data || exit 1
rm -rfv tmp || exit 1
