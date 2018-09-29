from flask.views import MethodView

from flask import (
    render_template,
    request,
    redirect,
    url_for,
)


import os


class UploadTestFile(MethodView):
    def get(self):
        return render_template('upload_test_file.html')

    def post(self):
        # check if the post request has the file part
        if 'filename' not in request.files:
            return redirect(request.url)
        file = request.files['filename']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        file.save(os.path.join('.', file.filename))
        return f'Uploaded {file.filename}'
