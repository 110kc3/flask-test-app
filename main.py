#! /usr/bin/env python
import os
from app import app
app = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), debug=True) # run app in debug mode on port 8080

