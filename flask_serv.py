from flask import Flask, render_template,url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from web_scraping import web_scrape
from threading import Thread
from flask import redirect





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

def webScrapeWithDB(id,db,url,email):
    try:
        web_scrape(url,email)
    except:
        print("error has occured")
    monitor = Monitor.query.get(id)
    monitor.status = 0
    db.session.commit()




class Monitor(db.Model):
    id = db.Column(db.Integer,primary_key=True )
    url = db.Column(db.String(512), nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Integer, default=0)
    name = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(512),nullable=False)
    email = db.Column(db.String(512),nullable=False)


    def __repr__(self):
        return '<Task %r>' % self.id

    def __init__(self,url,status,name,description,email):
        self.url = url
        self.status = status
        self.name = name
        self.description = description
        self.email = email


@app.route('/',methods=['POST','GET'])

def index():
    if request.method == 'POST':
        url = request.form['url']
        name = request.form['ime']
        opis = request.form['opis']
        email = request.form['email']
        new_monitor = Monitor(url,1,name,opis,email)
        try:
            
            db.session.add(new_monitor)
            db.session.commit()
            new_thread = Thread(target=webScrapeWithDB,args=(new_monitor.id,db,url,email))
            new_thread.start()
            return redirect('/')
        except Exception as err:
            print(err)
            return str(err)


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
        opis = request.form['opis']
        email = request.form['email']        
        new_monitor = Monitor(url,1,name,opis,email)
        #new_thread = Thread(target=web_scrape,args=(url,email))
        
        try:
            
            db.session.add(new_monitor)
            db.session.commit()
            new_thread = Thread(target=webScrapeWithDB,args=(new_monitor.id,db,url,email))
            new_thread.start()
            return redirect('/')
        except Exception as err:
            print(err)
            return str(err)
        
        #return render_template('index.html')

    else:
        monitors = Monitor.query.order_by(Monitor.date_created).all()
        return render_template('index.html',monitor=monitors)

@app.route('/delete', methods = ['GET'])
def delete():
    id = request.args.get('id')
    element = Monitor.query.get(id)
    db.session.delete(element)
    db.session.commit()
    return redirect('/')

@app.route('/run', methods = ['GET'])
def run():
    id = request.args.get('id')
    element = Monitor.query.get(id)
    element.status = 1
    db.session.commit()
    new_thread = Thread(target=webScrapeWithDB,args=(id,db,element.url,element.email))
    new_thread.start()
    return redirect('/')



    
if __name__ == "__main__":
    app.run(debug=True)