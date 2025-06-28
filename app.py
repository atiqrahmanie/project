from flask import flash,  render_main, request, redirect, url_for
from models import db, Passenger
import qrcode
import os


# crete the flask app
app = Flask(__name__)

# data base configure

app.config[ 'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/airportdb'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

#Database Initilization with app
db.init_app(app)

# crete table manually before first request

with app.app_context():
    db.create_all()
    os.makedirs("static/qr_codes" , exist_ok=True)


    from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Welcome TO Smart Boardind System"
    app.run(debug=True)