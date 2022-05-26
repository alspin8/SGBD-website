from db.src.statsHandle import get_stats
from flask import Blueprint, render_template, request, redirect, url_for

stats = Blueprint('stats', __name__)

@stats.route('/')
def index():
    stats = get_stats()
    return render_template('stats.index.html', stats=stats)