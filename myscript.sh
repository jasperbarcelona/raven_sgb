#!/bin/bash
. venv/bin/activate
export DATABASE_URL='sqlite:///local.db'
export PORT=80
python admin.py