from flask import render_template, flash, redirect, url_for, request
from flask import copy_current_request_context
from app import app
from app.forms import SearchForm
from app.email import send_mail
from app import db
# from flask_mail import Message
from app.models import AppData
import threading


@app.route('/')
@app.route('/index')
def index():
    city_str = 'Bs As'
    return render_template('index.html', title='Index', city_str=city_str)


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        print("DATA FORM:", form.search_item.data)
        search_street = form.search_item.data
        search_street = search_street.title()
        street_data = AppData(street_search=search_street)
        db.session.add(street_data)
        db.session.commit()

        @copy_current_request_context
        def send_msg(street_search, timestamp):
            send_mail(street_search, timestamp)

        sender = threading.Thread(name='mail_sender',
                                  target=send_msg,
                                  args=(street_data.street_search, street_data.timestamp))

        sender.start()

        return render_template("info_street.html",
                                geo_street=search_street,
                              )

    return render_template("search.html", title="Search", form=form)


@app.route('/list')
def list():
    page = request.args.get('page', 1, type=int)
    cities_list = AppData.query.order_by(AppData.timestamp.desc()).paginate(
        page, app.config['ITEMS_PER_PAGE'], False)
    next_url = url_for('list', page=cities_list.next_num) \
        if cities_list.has_next else None
    prev_url = url_for('list', page=cities_list.prev_num) \
        if cities_list.has_prev else None
    return render_template('list.html', title='Lista', cities_list=cities_list.items, next_url=next_url, prev_url=prev_url)
