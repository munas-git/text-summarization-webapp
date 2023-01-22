#!/usr/bin/env bash
# exit on error
set -o errexit

pip install gunicorn
pip install --upgrade pip
pip install -r requirements.txt