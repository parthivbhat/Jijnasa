#!/bin/bash

cd /home/parthiv_setu/jijnasa
source .venv/bin/activate

echo "=== JIJNASA DAILY NEWS ==="
date

python -u jijnasa.py news
