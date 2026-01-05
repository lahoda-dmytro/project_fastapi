#!/usr/bin/env bash
# exit on error
set -o errexit

# build frontend
cd frontend
npm install
npm run build
cd ..

# install backend requirements
pip install -r requirements.txt
