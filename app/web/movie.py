from flask import request, jsonify, render_template

from app.db_master import mongo
from app.forms import movie
from app.forms.movie import SearchForm
from . import web


@web.route('/movie/play')
def play():
    _id = request.args.get('_id')
    mv = mongo.search_play_detail(_id)
    return render_template('search.html', mv=mv)


@web.route("/movie/search")
def search():
    form = SearchForm(request.args)
    if form.validate():
        q = form.page.data
        page = form.page.data
    else:
        pass
        # return render_template('search.html', data=[1, 2, 3])
    return "hello"

