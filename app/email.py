from flask import render_template
from flask_mail import Message
from app import mail


def send_mail(street_search, timestamp):
    msg = Message(f'Se busco la calle: {street_search}',
                  sender='heyheymycode@gmail.com',
                  recipients=['heyheymycode@gmail.com'])
    msg.html = render_template('email.html',
                               street_search=street_search,
                               timestamp=timestamp)

    mail.send(msg)
