from flask.views import MethodView

from flask import (
    render_template
)
import datetime


class Index(MethodView):
    def get(self):
        return render_template('index.html', time=datetime.datetime.now())
