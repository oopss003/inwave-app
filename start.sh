#!/bin/bash
gunicorn -b 0.0.0.0:$PORT flask_server:app
