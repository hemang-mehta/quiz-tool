from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from Web_scrapping import gfg_ques_retrieval

file = open('mongo_url.txt')
mongo_url, sk = file.readlines()
mongo_url = mongo_url.strip()
sk = sk.strip()
client = MongoClient(mongo_url)
file.close()

collection = client['MCQ-tool']
User_login_data = collection['User_login_data']
User_score_data = collection['User_score_data']
q_db = collection['Questions_database']

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydata"
app.secret_key = sk

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user' in session:
        user = session['user']
        return redirect(url_for('userpage'))
    else:
        if request.method == 'POST':
            button_clicked = request.form['enter']
            if button_clicked == 'login':
                user = None
                return redirect(url_for('login'))
            elif button_clicked == 'signup':
                user = None
                return redirect(url_for('signup'))
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
            if name == "admin":
                return redirect(url_for('adminpage'))
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
        if name == "" or password == "":
            error = "Enter both Name and Password."
        elif User_login_data.find_one({'name': name}):
            error = "You already have an account"
        else:
            User_login_data.insert_one({'name':name, 'password':password})
            User_score_data.insert_one({'name': name, 'test_scores': {'Easy':[],'Medium':[],'Hard':[]}})
        if error == None:
            return render_template('login.html')
    return render_template('signup.html', error=error)

@app.route('/adminpage', methods=['GET', 'POST'])
def adminpage():
  if request.method == 'POST':
    button_clicked = request.form['button_clicked']
    if button_clicked == 'QDB':
      return redirect(url_for('qdb'))
    elif button_clicked == 'GNQ':
      num_links = request.form['numlinks']
      gfg_ques_retrieval.scrape_questions(num_links)
      flash('Website scrapped successfuly!!!', 'info')
      return render_template('adminpage.html')
    else:
      return render_template('adminpage.html')
  if session['user'] == 'admin':
    return render_template('adminpage.html')
  else:
      return redirect(url_for('logout'))


@app.route('/qdb', methods=['GET', 'POST'])
def qdb():
    if session['user'] == 'admin':
        q = list(q_db.find({}))
        if request.method == 'POST':
            button_clicked = request.form['submit']
            if button_clicked=='savechanges':
                new_diff_lvl = request.form.to_dict()
                new_diff_lvl.pop('submit', None)
                for id, d_lvl in new_diff_lvl.items():
                    q_db.update_one({'_id': ObjectId(id)}, {'$set': {'difficulty': int(d_lvl)}})
                flash('Questions updated successfuly!!!', 'info')
                return redirect(url_for('adminpage'))
            else:
                return redirect(url_for('adminpage'))
        return render_template('question_db.html', database = q)
    else:
        return redirect(url_for('signup'))

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
        if user == "admin":
            return redirect(url_for('adminpage'))
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