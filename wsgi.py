# app = create_app('testing')
import logging
import os
import sys

from app import app

if __name__ == "__main__":
    application = app
    # app.run(host="0.0.0.0", debug=True, ssl_context='adhoc',port=80)
    app.run(host="0.0.0.0")
