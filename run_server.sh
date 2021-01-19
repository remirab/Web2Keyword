#!/bin/bash

# TODO Set number of workers right for production ! IMPORTANT
gunicorn wsgi:app --workers 5 --bind 127.0.0.1:5000 --timeout 120