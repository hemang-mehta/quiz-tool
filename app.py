from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from pymongo import MongoClient

client = MongoClient('mongodb+srv://hemangmehta1703:hemang@mcq-tool.orytooa.mongodb.net/?retryWrites=true&w=majority&appName=MCQ-tool')

collection = client['MCQ-tool']
user_data = collection['User_data']

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydata"
app.secret_key = "quiz-tool.."

@app.route('/')
def home():
    if 'user' in session:
        user = session['user']
    else:
        user = None
    return render_template('homepage.html', user_auth = user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        if user_data.find_one({'name': name, 'password': password}):
            session['user'] = name
            return redirect(url_for('userpage'))
        else:
            error = "Incorrect userID or password."
        if error != None:
            return render_template('login.html', error=error)
    else:
        if "user" in session:
            return redirect(url_for('userpage'))
    return render_template('login.html', error=None)

@app.route('/signup',methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        if user_data.find_one({'name': name}):
            error = "You already have an account"
        else:
            user_data.insert_one({'name':name, 'password':password})
        if error == None:
            return render_template('login.html')
    return render_template('signup.html', error=error)

@app.route('/aboutus')
def aboutus():
    if 'user' in session:
        user = session['user']
    else:
        user = None
    return render_template('aboutus.html', user_auth = user)

@app.route('/contactus')
def contactus():
    if 'user' in session:
        user = session['user']
    else:
        user = None
    return render_template('contactus.html', user_auth = user)

@app.route('/userpage')
def userpage():
    if 'user' in session:
        user = session['user']
        u_data = user_data.find({})
        return render_template('userpage.html', user_auth = user, u_data = u_data)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)