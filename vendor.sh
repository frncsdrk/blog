#!/usr/bin/env bash
#
# create vendor dir

mkdir -p vendor/spectre.css
cp -R node_modules/spectre.css/dist/* vendor/spectre.css
