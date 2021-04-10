#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

# Index data
python3 migrate_restaurant.py
python3 migrate_data.py

# Install aspect model
cd aspect_model/
python3 download_model.py

# Install and build frontend
cd ../frontend
npm install
npm run build
