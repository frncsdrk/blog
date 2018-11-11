#!/usr/bin/env bash

./build.py

echo "checking out gh-pages"
git checkout gh-pages
git merge master
git push origin gh-pages

echo "DEPLOYED!"

git checkout master
git branch
