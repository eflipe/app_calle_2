from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    city_str = 'Bs As'
    return render_template('index.html', title='Index', city_str = city_str)
