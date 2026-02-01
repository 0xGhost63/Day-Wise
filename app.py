import json
import random
from flask import Flask,render_template,url_for,redirect,request,flash,session
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from datetime import datetime,timedelta

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
    edited = db.Column(db.Boolean, default=False)  

    

    def __init__(self,title,content,user_id):
        self.title=title
        self.content=content
        self.user_id=user_id
        self.edited = False



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


    ##Calculating the Streak ...
    streak_counter = 0
    today = datetime.now().date()

    listt = Diary.query.filter_by(user_id=user.id).order_by(Diary.diary_time.desc()).all()

    # taking only the dates
    diary_dates = list({ d.diary_time.date() for d in listt })


    current_day = today

    for date in diary_dates:
        if date==current_day:
            streak_counter+= 1
            current_day =current_day-timedelta(days=1)

    current_date=datetime.now().strftime('%Y %m %d')

    return render_template('home.html',current_date=current_date,username=username,quote=quote,author=author,total_entries=leng,this_month=this_month_counter,streak_days=streak_counter)


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


@app.route('/journal')
def journal():

    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    if not user:
        session.clear()
        return redirect(url_for('login'))

    entries = user.diaries
    total_entries = len(entries)

    return render_template('journal.html',total_entries=total_entries,entries=entries)

@app.route('/view-entry/<int:entry_id>')
def view_entry(entry_id):
    entry = Diary.query.get_or_404(entry_id)
    # Check if entry belongs to current user
    if entry.user_id != session.get('user_id'):
        return redirect(url_for('home'))
    
    return render_template('view_entry.html', entry=entry)


@app.route('/delete-entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = Diary.query.get_or_404(entry_id)
    # Security check
    if entry.user_id != session.get('user_id'):
        return redirect(url_for('home'))
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('journal'))


@app.route('/edit-entry/<int:entry_id>', methods=['GET','POST'])
def edit_entry(entry_id):
    entry = Diary.query.get_or_404(entry_id)
    current_date=datetime.now().strftime("%Y %m %d")

    if entry.user_id != session.get('user_id'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        entry.title = request.form.get('title')
        entry.content = request.form.get('content')
        entry.edited = True               # flag as edited
        entry.diary_time = datetime.now() # optional: update timestamp
        db.session.commit()
        flash("Diary updated!")
        return redirect(url_for('view_entry', entry_id=entry.id))

    return render_template('edit_entry.html', entry=entry,current_date=current_date)





@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



if __name__=="__main__":
    print("Hello World")

    app.run(debug=True)
    with app.app_context():
        db.create_all()
