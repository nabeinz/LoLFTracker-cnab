from datetime import datetime

import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key ="Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/lo_lf_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


#Creating model table for our CRUD database
class associates(db.Model):
    __tablename__ = 'associates'
    badge_barcode_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    employee_name = db.Column(db.String(100))



class data(db.Model):
    badge_barcode_id = db.Column(db.Integer, primary_key = True)
    employee_name = db.Column(db.String(100))
    amazon_id = db.Column(db.String(100))
    date = db.Column(db.String(100))
    lolf = db.Column(db.String(100))

    def __init__(self, badge_barcode_id, employee_name,amazon_id, date, lolf):
        self.badge_barcode_id = badge_barcode_id
        self.employee_name = employee_name
        self.amazon_id = amazon_id
        self.date = date
        self.lolf = lolf


@app.route('/')
def Index():

    return render_template("index.html")


@app.route('/checkin', methods = ['GET', 'POST'])

def checkin():


        badge_barcode_id = request.form['badge_barcode_id']
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")
        lolf = request.form['lolf']

        try:
            name = db.session.query(associates.employee_name).filter(associates.badge_barcode_id == badge_barcode_id ).all()
            print(name[0][0])

            user_id = db.session.query(associates.user_id).filter(associates.badge_barcode_id == badge_barcode_id ).all()
            print(user_id[0][0])

            associate_data = data(badge_barcode_id, name[0][0] , user_id[0][0] , now.strftime("%d/%m/%Y %H:%M:%S"), lolf)
            db.session.add(associate_data)

            db.session.commit()
            flash(lolf+" Driver \""+ user_id[0][0]+ "\" Checked In Succcessful")

            return redirect(url_for('Index'))
        except:
            flash(badge_barcode_id + " Associate Not Found")
            return redirect(url_for('Index'))




@app.route('/fetch')
def fetch():
    all_data = data.query.all()
    return render_template("display.html", data = all_data)






if __name__ == '__main__':
   app.run(debug=True)