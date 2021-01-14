from flask import render_template, flash, redirect, url_for
from flask import copy_current_request_context
from app import app
from app.forms import SearchForm
from app import db
from app import mail
from flask_mail import Message
from app.models import AppData
import threading


def send_mail(street_search, timestamp):
    msg = Message(f'Se busco la calle: {street_search}',
                  sender='heyheymycode@gmail.com',
                  recipients=['heyheymycode@gmail.com'])
    msg.html = render_template('email.html',
                            street_search=street_search,
                            timestamp=timestamp)

    mail.send(msg)


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
                                  args = (street_data.street_search, street_data.timestamp))

        sender.start()

        return render_template("info_street.html",
                                geo_street=search_street,
                                )

    return render_template("search.html", title="Search", form=form)
