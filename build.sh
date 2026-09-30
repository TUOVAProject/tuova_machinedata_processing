#!/bin/bash

rm -rf ./build
mkdir -p ./build

cp -r ./src ./config.json ./*.py ./pyproject.toml ./README.md ./build
rm -rf ./build/src/tuova_machinedata_processing/__pycache__
