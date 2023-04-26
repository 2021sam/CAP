#!/bin/bash

source /home/x/CAP/env/bin/activate
gunicorn -c /home/x/CAP/conf/gunicorn_cap.py cap.wsgi
