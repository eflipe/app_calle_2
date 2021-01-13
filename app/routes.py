from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SearchForm
from app import db
from app.models import AppData


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
        print("DATA FORM", form.search_item.data)
        search_street = form.search_item.data
        search_street = search_street.title()
        street_data = AppData(street_search=search_street)
        db.session.add(street_data)
        db.session.commit()
#        busqueda_calle = request.form['search_item'] # name="search_item"


        return render_template("info_street.html",
                                geo_street=search_street,
                                )

    return render_template("search.html", title="Search", form=form)
