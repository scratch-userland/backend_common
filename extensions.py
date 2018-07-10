# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_bcrypt import Bcrypt
from flask_celery import Celery
from flask_wtf.csrf import CSRFProtect

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
celery = Celery()
