from flask import render_template, flash, redirect, url_for, request
from flask import copy_current_request_context
from app import app
from app.forms import SearchForm
from app.email import send_mail
from app.txt_search import search_calle
from app.wiki_search import CalleClass
from app.api_here import api_here
from app import db
# from flask_mail import Message
from app.models import AppData
import threading


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        calle_lat = request.form['lat_url_1']
        calle_long = request.form['long_url_2']
        print(calle_lat, calle_long)
        context = api_here(calle_lat, calle_long)

        if context[0] == 400:
            street_data = AppData(street_geo=context[1])
            db.session.add(street_data)
            db.session.commit()
            return render_template("info_street.html", info_street=context[1])

        if context[0] != 400:
            street_data = AppData(street_geo=context[3])

        db.session.add(street_data)
        db.session.commit()

        search_street = context[5]
        search_info = search_calle(search_street)
        msg_wiki = "*Info obtenida de la base de datos."

        wiki_info = CalleClass(search_street.title())

        if not search_info:
            print("No encontrado")
            search_info = wiki_info.load_calle()
            msg_wiki = "*Datos obtenidos desde Wikipedia, pueden \
                       no coincidir con su búsqueda."

            print("INFO WIKI", search_info)

        wiki_link = wiki_info.wiki_calle()
        return render_template("info_street.html",
                                geo_street=search_street,
                                info_street=search_info,
                                msg_wiki=msg_wiki, wiki_link=wiki_link,
                                api_key=context[0], address=context[3],
                                lat_str=calle_lat, long_str=calle_long)

    city_str = 'App Calles'
    return render_template('index.html', title='Index', city_str=city_str)


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        print("SEARCH FORM:", form.search_item.data)
        search_street = form.search_item.data
        search_street = search_street.title()
        street_data = AppData(street_search=search_street)
        db.session.add(street_data)
        db.session.commit()

        search_info = search_calle(search_street)
        msg_wiki = "*Info obtenida de la base de datos."
        search_street_title = search_street.title()
        print("TITLE", search_street_title)
        wiki_info = CalleClass(search_street_title)

        if not search_info:
            print("No encontrado")
            search_info = wiki_info.load_calle()
            msg_wiki = "*Datos obtenidos desde Wikipedia, pueden \
                       no coincidir con su búsqueda."

            print("INFO WIKI", search_info)

        wiki_link = wiki_info.wiki_calle()

        @copy_current_request_context
        def send_msg(street_search, timestamp):
            send_mail(street_search, timestamp)

        sender = threading.Thread(name='mail_sender',
                                  target=send_msg,
                                  args=(street_data.street_search, street_data.timestamp))

        sender.start()

        return render_template("info_street.html",
                                geo_street=search_street,
                                info_street=search_info,
                                msg_wiki=msg_wiki,
                                wiki_link=wiki_link
                               )

    return render_template("search.html", title="Búsqueda", form=form)


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
