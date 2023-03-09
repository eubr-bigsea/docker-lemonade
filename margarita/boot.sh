#!/bin/bash
exec gunicorn --config gunicorn_config.py margarita:app