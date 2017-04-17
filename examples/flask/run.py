#!/usr/bin/env python
import os

from app import app, db

db.create_all()

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
