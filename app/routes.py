from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SearchForm


@app.route('/')
@app.route('/index')
def index():
    city_str = 'Bs As'
    return render_template('index.html', title='Index', city_str=city_str)


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():

        flash('Buscaste la calle {}'.format(form.search_item.data))

        return redirect(url_for('index'))

    return render_template("search.html", title="Search", form=form)
