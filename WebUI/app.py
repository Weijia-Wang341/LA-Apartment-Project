from flask import Flask,render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user, login_required, logout_user, current_user,UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import requests
import json
import os
import re

app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SECRET_KEY'] = 'hjshjhdjahkjshkjdhjs'
db.init_app(app)
picFolder = os.path.join('static', 'pics')
app.config['UPLOAD_FOLDER'] = picFolder

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'], 'login_pic.svg')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", login_image=pic2,user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('home'))

    return render_template("sign_up.html", user=current_user)

@app.route('/')
@login_required
def home():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'la.svg')
    return render_template("home.html", home_image=pic1, user=current_user)

@app.route('/apartment',methods=['GET', 'POST'])
def apartment():
    url = ' https://dsci551-bd054-default-rtdb.firebaseio.com/.json'
    data = requests.get(url)

    final = data.content.decode('utf8')
    load = json.loads(final)

    df = pd.DataFrame(load)
    
    if request.method == 'POST':
        num_of_bed= request.form.get('numberofbedrooms')
        priceMin = request.form.get('priceRangeMin')
        priceMax = request.form.get('priceRangeMax')
        info = request.form.get('info')

        
        if num_of_bed=='studio':
            df=df[df['Bed'].str.contains('Studio')]
            
        elif num_of_bed=='1':
            df=df[~ df['Bed'].str.contains('Studio')]
            
            judge=[(len(i)==1 and i[0]=='1') or (len(i)==2 and int(i[0])<=1<=int(i[1])) for i in df['Bed'].str.findall('\d')] 
            df=df[judge]

        elif num_of_bed=='2':
            df=df[~ df['Bed'].str.contains('Studio')]
            judge=[(len(i)==1 and i[0]=='2') or (len(i)==2 and int(i[0])<=2<=int(i[1])) for i in df['Bed'].str.findall('\d')] 
            df=df[judge]
        
        elif num_of_bed=='3':
            df=df[~ df['Bed'].str.contains('Studio')]
            judge=[(len(i)==1 and i[0]=='3') or (len(i)==2 and int(i[0])<=3<=int(i[1])) for i in df['Bed'].str.findall('\d')] 
            df=df[judge]
        
        elif num_of_bed=='4':
            df=df[df['Bed'].str.contains('4')]

        if info=='Dog Firendly':
            df=df[df['Info'].str.contains('Dog',case=False, na=False)]

        elif info=='Cat Firendly':
            df=df[df['Info'].str.contains('Cat',case=False, na=False)]

        elif info=='Washer':
            df=df[df['Info'].str.contains('Washer',case=False, na=False)]

        elif info=='Parking':
            df=df[df['Info'].str.contains('Parking', case=False, na=False)]

        elif info=='Dishwasher':
            df=df[df['Info'].str.contains('Dishwasher',case=False, na=False)]

        elif info=='Fitness Center':
            df=df[df['Info'].str.contains('Fitness',case=False, na=False)]
        

        if priceMin!='' and priceMax!='':
            dfRange=[(len(i)==2 and int(i[0])>=int(priceMin) and int(i[1])<=int(priceMax)) for i in df['Price'].replace(to_replace='\$',value='',regex=True).replace(to_replace='\,',value='',regex=True).str.findall('\d+')]
            df=df[dfRange]

        elif priceMin!='' and priceMax=='':
            minPrice=[(len(i)==2 and int(i[0])>=int(priceMin)) for i in df['Price'].replace(to_replace='\$',value='',regex=True).replace(to_replace='\,',value='',regex=True).str.findall('\d+')]
            df=df[minPrice]
        
        elif priceMax!='' and priceMin=='':
            maxPrice=[(len(i)==2 and int(i[1])<=int(priceMax)) for i in df['Price'].replace(to_replace='\$',value='',regex=True).replace(to_replace='\,',value='',regex=True).str.findall('\d+')]
            df=df[maxPrice]
        
    return render_template('apartment.html', tables=[df.to_html(classes='data')], titles=' ', user=current_user)

@app.route('/zillow',methods=['GET', 'POST'])
def zillow():
    url = ' https://second-dc4b8-default-rtdb.firebaseio.com/.json'
    data2 = requests.get(url)

    final2 = data2.content.decode('utf8')
    load2 = json.loads(final2)

    df2 = pd.DataFrame(load2)

    if request.method == 'POST':
        Zillowmin= request.form.get('ZillowMin')
        Zillowmax = request.form.get('ZillowMax')

        if Zillowmin!='' and Zillowmax!='':
            range=[(len(i)==1 and int(Zillowmax)>=int(i[0])>=int(Zillowmin)) for i in df2['Price'].str.replace(',','',True).str.findall('\d+')]
            df2=df2[range]

        elif Zillowmin!='' and Zillowmax=='':
            Min_price=[(len(i)==1 and int(i[0])>=int(Zillowmin)) for i in df2['Price'].str.replace(',','',True).str.findall('\d+')]
            df2=df2[Min_price]
            
        elif Zillowmax!='' and Zillowmin=='':
            Max_price=[(len(i)==1 and int(i[0])<=int(Zillowmax)) for i in df2['Price'].str.replace(',','',True).str.findall('\d+')]
            df2=df2[Max_price]

    return render_template('zillow.html', tables=[df2.to_html(classes='data')], titles=' ', user=current_user)

@app.route('/map')
def map():
    return render_template("index.html", user=current_user)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

if __name__ == '__main__':
    app.run(debug=True)
