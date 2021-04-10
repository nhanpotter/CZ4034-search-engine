#!/bin/bash

cd sentiment_model/
mkdir -p .venv/
pipenv install --dev
source .venv/bin/activate
python3 bin/download_model
