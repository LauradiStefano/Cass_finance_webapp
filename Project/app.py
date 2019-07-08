import os

from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

UPLOAD_DIR = 'uploads/'

# Allowed file types for file upload

ALLOWED_EXTENSIONS = set(['xlsx'])

app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.secret_key = 'MySecretKey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

if not os.path.isdir(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)


def allowed_file(filename):
    """Does filename have the right extension?"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
