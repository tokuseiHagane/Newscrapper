from flask import Blueprint, Flask, render_template, request, url_for, flash, redirect
from .. import logger
from models.ArticleModel import Article
from models.SourceModel import Source

views = Blueprint('views', __name__)


@views.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)
