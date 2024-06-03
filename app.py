from bson import ObjectId
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from pymongo import MongoClient

client = MongoClient('mongodb+srv://hemangmehta1703:hemang@mcq-tool.orytooa.mongodb.net/?retryWrites=true&w=majority&appName=MCQ-tool')

collection = client['MCQ-tool']
User_login_data = collection['User_login_data']
User_score_data = collection['User_score_data']
q_db = collection['Questions_database']

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
        if User_login_data.find_one({'name': name, 'password': password}):
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
        if User_login_data.find_one({'name': name}):
            error = "You already have an account"
        else:
            User_login_data.insert_one({'name':name, 'password':password})
            User_score_data.insert_one({'name': name, 'test_scores': {'Easy':[],'Medium':[],'Hard':[]}})
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

@app.route('/userpage', methods=['POST', 'GET'])
def userpage():
    if 'user' in session:
        user = session['user']
        if request.method == 'POST':
            diff = request.form.get('difficulty_level')
            return redirect(url_for('quizpage', difficulty_lvl = diff))
        return render_template('userpage.html', user_auth = user, user_score_data = User_score_data.find_one({'name':user}))
    else:
        return redirect(url_for('login'))

@app.route('/quizpage', methods = ['POST', 'GET'])
def quizpage():
    if 'user' in session:
        user = session['user']
        if request.method == 'GET':
            diff_lvl = request.args.get('difficulty_lvl')
            diff_dict = {'Easy': 1, 'Medium': 2, 'Hard': 3}
            ques_data = list(q_db.find({'difficulty': diff_dict[diff_lvl]}).limit(20))
            return render_template('quizpage.html', userid = user, ques_data = ques_data, difficulty_level = diff_lvl)
        if request.method == 'POST':
            user_answers = request.form.to_dict()
            score = 0
            ans_dict = {'1':"A", '2':"B", '3':"C", '4':"D"}
            diff_lvl = ''
            for q_id, user_answer in user_answers.items():
                question = q_db.find_one({"_id": ObjectId(q_id)})
                diff_lvl = question.get('difficulty')
                if question and question.get('correct_ans') == ans_dict[user_answer]:
                    score += 1
            diff_dict = { 1:'Easy',  2:'Medium',  3:'Hard'}
            diff_lvl = diff_dict[diff_lvl]
            User_score_data.update_one({'name': session['user']}, {"$push": {f'test_scores.{diff_lvl}': score}})
            return redirect(url_for('userpage'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)