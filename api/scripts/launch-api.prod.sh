#!/usr/bin/env bash

python -m alembic upgrade head
python -m uvicorn taskmasterexp.app:app --host 0.0.0.0 --port $PORT
