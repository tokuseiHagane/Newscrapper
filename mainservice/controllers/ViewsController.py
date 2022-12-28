from flask import Blueprint, Flask, render_template, request, url_for, flash, redirect
import time
import datetime
from app.models.ArticleModel import Article
from app.models.SourceModel import Source
from app.controllers.SetupController import database, logger
from rich.pretty import pprint as print
base_ranges = {'1': "false", '3': "false", '7': "false", '30': "false", 'all': "true"}

views = Blueprint('views', __name__, template_folder='/app/view', static_folder='/app/view/static', static_url_path='/static')

article_model = Article()


@views.route('/', methods=['POST', 'GET'])
def index():
    kwargs = {'db': database}
    new_ranges = base_ranges.copy()
    kwargs['time_range'] = str(request.form.get('time_range')) if request.form.get('time_range') is not None else -1
    kwargs['sources'] = [int(source) for source in request.form.get('sources')] if request.form.get('sources') is not None else [1,2,3,4,5,6,7]
    kwargs['source_types'] = request.form.get('source_types') or ['tg', 'rss']
    kwargs['offset'] = int(request.form.get('offset')) if request.form.get('offset') is not None else 0
    if 'time_range' in kwargs.keys() and kwargs['time_range'] != 'all':
        for key in base_ranges.keys():
            new_ranges[key] = "false" if key != kwargs['time_range'] else "true"
        kwargs['time_range'] = int(kwargs['time_range'])
        kwargs['start_time'] = datetime.datetime.strptime(request.form.get('start_time'),
                                                          "%Y-%m-%d %H:%M:%S").timestamp() if request.form.get('start_time') is not None \
                                                                                           else int(time.time()) 
                                     
    records = article_model.get_articles(**kwargs)
    kwargs.update(new_ranges)
    return render_template('index.html', records=records, **kwargs)
