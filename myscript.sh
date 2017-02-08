#!/bin/bash
. venv/bin/activate
export DATABASE_URL='sqlite:///local.db'
export PORT=5000
python admin.py