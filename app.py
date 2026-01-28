from flask import Flask,render_template
from dotenv import load_dotenv
import os


app=Flask(__name__)
load_dotenv()

admin_code = os.getenv("ADMIN_KEY")
@app.route('/',methods=['POST','GET'])
def home():
    return render_template("index.html",admin_code=admin_code)

if __name__=="__main__":
    app.run(debug=True)