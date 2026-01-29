import json
import random
from flask import Flask,render_template,url_for,redirect,request,flash,session
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from datetime import datetime

app=Flask(__name__)

load_dotenv()
admin_code = os.getenv("ADMIN_KEY")
app.secret_key = os.urandom(24)


app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Users_Data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)

## loading the quotes from the json file into a list
with open('quotes.json',"r",encoding="utf-8") as f:
    quotes=json.load(f)
    
class User(db.Model):

    __tablename__="users"

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(23),nullable=False)
    email=db.Column(db.String(50),nullable=False,unique=True)
    pwd=db.Column(db.String(128),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)  
    diaries=db.relationship('Diary',backref='users',lazy=True)

    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd = self.hash_password(pwd)

    @staticmethod
    def hash_password(pwd):
        return bcrypt.generate_password_hash(pwd).decode('utf-8')

    def check_password(self,pwd):
        return bcrypt.check_password_hash(self.pwd, pwd)




class Diary(db.Model):
    __tablename__ = "diaries"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    diary_time=db.Column(db.DateTime  , default=lambda: datetime.now().replace(second=0, microsecond=0))
    content=db.Column(db.Text,nullable=False)
    

    def __init__(self,title,content,user_id):
        self.title=title
        self.content=content
        self.user_id=user_id


@app.route('/',methods=['POST','GET'])
def login():
    if request.method=='POST':
        user_data=request.form.get('username')
        pwd=request.form.get('password')

        user=User.query.filter_by(username=user_data).first()

        if(user==None):
            user=User.query.filter_by(email=user_data).first()
        
        if user and user.check_password(pwd):
            session['user_id'] = user.id   
            return redirect(url_for('home'))
        
        else:
            flash("Invalid Username or Password")
            return render_template('login.html')

    return render_template("login.html")


@app.route('/signup',methods=['POST','GET'])
def register():
    
    if request.method=='POST':

        username=request.form.get('username')
        email=request.form.get('email')
        pwd=request.form.get('password')
        con_pwq=request.form.get('confirm_password')

        usr_check=User.query.filter_by(username=username).first()

        check1=False
        check2=False

        if(usr_check!=None):
            flash(f"User with username : {username} already exists ! Choose another username :) ")
        else:
            check1=True

        if(pwd==con_pwq):
            check2=True
        else:
            flash(f"Both passwords should exactly match ! :)")

        
        if (check1 and check2 ):
            newUser=User(email=email,pwd=pwd,username=username)
            db.session.add(newUser)   
            db.session.commit()   
            flash("Successfully Created the Account !")    
            return redirect(url_for('login'))
        

    return render_template('registration.html')


@app.route('/home',methods=["GET"])
def home():


    #quote
    quote_obj=random.choice(quotes)
    quote=quote_obj['quote']
    author=quote_obj['author']

    user_id=session.get('user_id')
    user=User.query.get(user_id)
    if not user:
        session.clear()
        return redirect(url_for('login'))
    



    username=user.username
    entries=user.diaries
    
    # total entries
    leng = len(entries)

    #this month entries
    now=datetime.now()
    this_month=now.month

    listt=Diary.query.filter_by(user_id=user.id).order_by(Diary.diary_time).all()
    diary_times=[d.diary_time for d in listt]
     
    ## it returns data lik this ::
    # 2026-01-29 21:01:00
    # 2026-01-29 21:11:00

    ## and month returns like : 
    # 1

    this_month_counter=0

    for time in diary_times:
        if time.month==this_month:
            this_month_counter=this_month_counter+1

    



    return render_template('home.html',username=username,quote=quote,author=author,total_entries=leng,this_month=this_month_counter)


@app.route('/compose',methods=['GET','POST'])
def compose():
    now=datetime.now().strftime('%d %m %Y')
    if request.method=="POST":
        title=request.form.get('title')
        data=request.form.get('content')
        user_id=session.get('user_id')

        if not user_id:
            return redirect(url_for('login'))
        
        else:
            entry=Diary(title=title,user_id=user_id,content=data)
            db.session.add(entry)
            db.session.commit()
            flash("Sumbitted! :)")
            return redirect(url_for('home'))
    
    return render_template('compose.html',current_date=now)


## add the journals method here !


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__=="__main__":
    print("Hello World")

    app.run(debug=True)
    with app.app_context():
        db.create_all()
