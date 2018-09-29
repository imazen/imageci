from flask import (
    Flask,
    g,
)

from .index import Index
from .upload_test_file import UploadTestFile

from .database import db_session

app = Flask(__name__, template_folder='templates')
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max size is 16 MB
app.config['UPLOAD_FOLDER'] = "."


@app.before_request
def before_request():
    g.db = db_session


app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=['GET'])


app.add_url_rule('/upload_test_file',
                 view_func=UploadTestFile.as_view('upload_test_file'),
                 methods=['GET', 'POST'])
