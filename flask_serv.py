from msilib.schema import Error
from django.shortcuts import redirect, render
from flask import Flask, render_template,url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from web_scraping import web_scrape





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

class Monitor(db.Model):
    id = db.Column(db.Integer,primary_key=True )
    url = db.Column(db.String(512), nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Integer, default=0)
    content = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(512), nullable=False)


    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['POST','GET'])

def index():
    if request.method == 'POST':
        url = request.form['url']
        name = request.form['ime']
        description = request.form['opis']
        new_monitor = Monitor(url=url,name=name, content=description,status=1)
        try:
            db.session.add(new_monitor)
            db.session.commit()
            return redirect('/')
        except:
            return 'There has been an issue'


        #return render_template('index.html')

    else:
        monitors = Monitor.query.order_by(Monitor.date_created).all()
        return render_template('index.html',monitor=monitors)    


@app.route('/add_monitor_page.html')
def monitor():
    return render_template('add_monitor_page.html')
@app.route('/index.html',methods = ['POST','GET'])
def index_1():
    if request.method == 'POST':
        url = request.form['url']
        name = request.form['ime']
        description = request.form['opis']
        new_monitor = Monitor(url=url,name=name,status=1,content=description)
        command = "py web_scraping.py '"+url +"' "+ "tit.sober33@gmail.com"
        
        try:
            web_scrape(url,"tit")
            db.session.add(new_monitor)
            db.session.commit()
            return redirect('/')
        except:
            
            return 'err'


        #return render_template('index.html')

    else:
        monitors = Monitor.query.order_by(Monitor.date_created).all()
        return render_template('index.html',monitor=monitors)


if __name__ == "__main__":
    app.run(debug=True)