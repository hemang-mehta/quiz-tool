from flask import Flask, render_template, request, redirect, url_for, session
import datetime
from pymongo import MongoClient
# from Web_scrapping import gfg_ques_retrieval

file = open('mongo_url.txt')
mongo_url, sk = file.readlines()
mongo_url = mongo_url.strip()
sk = sk.strip()
client = MongoClient(mongo_url)
file.close()

collection = client['MCQ-tool']
User_login_data = collection['User_login_data']
User_score_data = collection['User_score_data']
User_curr_score = collection['User_curr_score']
q_db = collection['Topic_wise_questions']
u_msg = collection['User_msgs']

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydata"
app.secret_key = sk

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user' in session:
        user = session['user']
        surname = session['surname']
        return redirect(url_for('userpage'))
    else:
        if request.method == 'POST':
            button_clicked = request.form['enter']
            if button_clicked == 'signup':
                user = None
                surname = None
                return redirect(url_for('signup'))
    user = None
    surname = None
    return render_template('homepage.html', surname = surname, userid = user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        emailid = request.form['emailid']
        password = request.form['password']
        if User_login_data.find_one({'emailid': emailid, 'password': password}):
            session['user'] = User_login_data.find_one({'emailid': emailid})['name']
            session['emailid'] = emailid
            session['surname'] = User_login_data.find_one({'emailid': emailid})['surname']
            if emailid == "admin":
                return redirect(url_for('adminpage'))
            return redirect(url_for('userpage'))
        else:
            error = "Incorrect Email-ID or password."
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
        surname = request.form['surname']
        password = request.form['password']
        emailid = request.form['emailid']
        exp = request.form['experience']
        if name == "" or password == "" or emailid=="" or exp=="":
            error = "Fill in all your details."
        elif User_login_data.find_one({'emailid': emailid}):
            error = "You already have an account"
        else:
            User_login_data.insert_one({'name':name, 'surname':surname, 'password':password, 'emailid': emailid, 'experience': exp})
            User_score_data.insert_one({'emailid': emailid, 'num_tests': 0, 'test_data':[], 'scores':[], 'date': [], 'time_taken': []})
        if error == None:
            session['user'] = name
            session['emailid'] = emailid
            session['surname'] = surname
            if name == "admin":
                return redirect(url_for('adminpage'))
            return redirect(url_for('userpage'))
    return render_template('signup.html', error=error)

@app.route('/adminpage', methods=['GET', 'POST'])
def adminpage():
  if request.method == 'POST':
    button_clicked = request.form['button_clicked']
    if button_clicked == 'QDB':
      return redirect(url_for('qdb'))
    # elif button_clicked == 'GNQ':
    #   num_links = request.form['numlinks']
    #   gfg_ques_retrieval.scrape_questions(num_links)
    #   flash('Website scrapped successfuly!!!', 'info')
    #   return render_template('adminpage.html', userid = session['user'], surname = session['surname'])
    elif button_clicked == 'US':
        return redirect(url_for('userstats'))
    else:
      return render_template('adminpage.html', userid = session['user'], surname = session['surname'])
  if session['user'] == 'admin':
    return render_template('adminpage.html', userid = session['user'], surname = session['surname'])
  else:
      return redirect(url_for('logout'))

@app.route('/userstats', methods=['GET', 'POST'])
def userstats():
    if request.method=='GET':
        user_data = list(User_score_data.find({}))
        login_data = list(User_login_data.find({}))
        return render_template('userstats.html', userid = session['user'], surname = session['surname'], 
                               u_data = user_data, u_login_data = login_data)

@app.route('/qdb', methods=['GET'])
def qdb():
    if session.get('user') == 'admin':
        q = list(q_db.find({}))  # Assuming q_db is defined elsewhere
        if 'page' not in session:
            session['page'] = 1
        per_page = 30
        total_questions = len(q)
        pages = total_questions // per_page + (1 if total_questions % per_page > 0 else 0)

        # Get the page number from the query parameter
        page = request.args.get('page', 1, type=int)
        session['page'] = page

        start = (page - 1) * per_page
        end = start + per_page
        questions_subset = q[start:end]

        return render_template('question_db.html',
                               database=questions_subset,
                               userid=session['user'],
                               surname=session['surname'],
                               page=page,
                               pages=pages)
    else:
        return redirect(url_for('signup'))

@app.route('/aboutus')
def aboutus():
    if 'user' in session:
        user = session['user']
        surname = session['surname']
    else:
        surname = None
        user = None
    return render_template('aboutus.html', surname = surname, userid = user)

@app.route('/contactus', methods=['POST', 'GET'])
def contactus():
    if 'user' in session:
        user = session['user']
        surname = session['surname']
    else:
        surname = None
        user = None
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        msg = request.form['message']
        u_msg.insert_one({'name': name, 'emailid': email, 'message':msg})
        return render_template('contactus.html', surname = surname, userid = user)
    return render_template('contactus.html', surname = surname, userid = user)

@app.route('/userpage', methods=['POST', 'GET'])
def userpage():
    if 'user' in session:
        user = session['user']
        surname = session['surname']
        if user == "admin":
            return redirect(url_for('adminpage'))
        else:
            if User_curr_score.find_one({'emailid': session['emailid']}):
                return render_template('userpage.html', test = 'remaining', userid = user, surname = surname, message = 'Complete the pending test first...')
        if request.method == 'POST':
            topics = request.form.getlist('topics')
            if topics == []:
                return render_template('userpage.html', surname = surname, userid = user)
            session['topics'] = topics
            ques_data = {}
            total_questions = 0
            for i in range(len(topics)):
                pipeline = [{'$match': {'category': topics[i]}},{'$sample': {'size': 4}}]
                for j in list(q_db.aggregate(pipeline)):
                    if topics[i] in ques_data.keys():
                        ques_data[topics[i]].append({j['q_no']: ""})
                        total_questions += 1
                    else:
                        ques_data[topics[i]] = []
            
            # Adding the question data in session to access it in quizpage route
            # Adding quesiton data in the format of -> {'topic': [q_no, q_no...]}
            q_data = {}
            for key, value in ques_data.items():
                q_data[key] = [int(list(item.keys())[0]) for item in value]
            session['ques_data'] = q_data
            def convert_keys_to_strings(d):
                if isinstance(d, dict):
                    return {str(k): convert_keys_to_strings(v) for k, v in d.items()}
                elif isinstance(d, list):
                    return [convert_keys_to_strings(i) for i in d]
                else:
                    return d
            ques_data = convert_keys_to_strings(ques_data)
            emailid = User_login_data.find_one({'name': session['user']})['emailid']
            User_curr_score.insert_one({'emailid': emailid,
                                        'test_state': False,
                                        'questions':ques_data,
                                        'start_date': datetime.datetime.now().strftime("%x"),
                                        'start_time': datetime.datetime.now()})
            User_score_data.update_one(filter={'emailid':emailid}, update={'$inc':{'num_tests':1}, '$push':{'test_data':ques_data, 'scores':0, 'date':datetime.datetime.now().strftime("%x"),'time_taken':-1}})
            session['current_index'] = 0
            return redirect(url_for('quizpage'))
        elif request.method == 'GET':
            if 'message' in request.args:
                return render_template('userpage.html', test = 'complete', userid = user, surname = surname, message = request.args.get('message'))
            
        return render_template('userpage.html', surname = surname, userid = user)
    else:
        return redirect(url_for('login'))

@app.route('/quizpage', methods = ['POST', 'GET'])
def quizpage():
    if 'user' in session:
        user = session['user']
        surname = session['surname']
        if request.method == 'GET':
            # Finding the quesiton from Topic_wise_questions using category and question number
            topic = session['topics'][int(session['current_index']/3)]
            q_no = session['ques_data'][session['topics'][int(session['current_index']/3)]][session['current_index']%3]
            ques_data = q_db.find_one({'category': session['topics'][0], 'q_no': session['ques_data'][session['topics'][0]][0]})
            ans = User_curr_score.find_one({'emailid': session['emailid']})['questions'][topic][session['current_index']%3][str(q_no)]
            total_questions = len(User_curr_score.find_one({'emailid': session['emailid']})['questions'])*3
            return render_template('quizpage.html',
                                   surname = surname,
                                   userid = user,
                                   ques_data = ques_data,
                                   total_questions=total_questions,
                                   current_index = session['current_index'],
                                   ans = ans)
        
        if request.method == 'POST':
            button_clicked = request.form['button_clicked']
            answer = request.form.get('answer')
            topic = session['topics'][int(session['current_index']/3)]
            q_no = session['ques_data'][session['topics'][int(session['current_index']/3)]][session['current_index']%3]
            ques_data = q_db.find_one({'category': topic, 'q_no': q_no})
            if answer:
                #Store answer in database
                User_curr_score.update_one(filter={'emailid':session['emailid'], 'test_state': False}, update={'$set': {f'questions.{topic}.{session['current_index']%3}.{q_no}':answer}})
                if button_clicked == 'submit':
                    #Update the last question...
                    new_data = User_curr_score.find_one({'emailid': session['emailid']})['questions']
                    time_taken = (datetime.datetime.now() - User_curr_score.find_one({'emailid': session['emailid']})['start_time']).total_seconds()
                    User_curr_score.delete_one({'emailid': session['emailid']})
                    # Get score
                    score = 0
                    for topic, user_inp in new_data.items():
                        for i in user_inp:
                            for q_no, user_ans in i.items():
                                if user_ans == q_db.find_one({'category': topic, 'q_no': int(q_no)})['answer']:
                                    score += 1

                    User_score_data.update_one(filter={'emailid': session['emailid']}, update={'$set': {f'test_data.{len(User_score_data.find_one({'emailid':session['emailid']})['test_data'])-1}': new_data,
                                                                                                        f'time_taken.{len(User_score_data.find_one({'emailid':session['emailid']})['time_taken'])-1}': time_taken,
                                                                                                        f'scores.{len(User_score_data.find_one({'emailid':session['emailid']})['scores'])-1}': score}})
                    return redirect(url_for('userpage', message = 'Thank you for giving the test.'))
                elif button_clicked=='previous':
                    session['current_index'] -= 1
                elif button_clicked=='next':
                    session['current_index'] += 1
                topic = session['topics'][int(session['current_index']/3)]
                q_no = session['ques_data'][session['topics'][int(session['current_index']/3)]][session['current_index']%3]
                ques_data = q_db.find_one({'category': topic, 'q_no': q_no})
                ans = User_curr_score.find_one({'emailid': session['emailid']})['questions'][topic][session['current_index']%3][str(q_no)]
                total_questions = len(User_curr_score.find_one({'emailid': session['emailid']})['questions'])*3
                return render_template('quizpage.html',
                                surname = surname,
                                userid = user,
                                ques_data = ques_data,
                                total_questions=total_questions,
                                current_index = session['current_index'],
                                ans = ans)
            else:
                error = 'Select an answer first!'
                if button_clicked=='previous':
                    session['current_index'] -= 1
                    error = None
                topic = session['topics'][int(session['current_index']/3)]
                q_no = session['ques_data'][session['topics'][int(session['current_index']/3)]][session['current_index']%3]
                ans = User_curr_score.find_one({'emailid': session['emailid']})['questions'][topic][session['current_index']%3][str(q_no)]
                topic = session['topics'][int(session['current_index']/3)]
                q_no = session['ques_data'][session['topics'][int(session['current_index']/3)]][session['current_index']%3]
                ques_data = q_db.find_one({'category': topic, 'q_no': q_no})
                total_questions = len(User_curr_score.find_one({'emailid': session['emailid']})['questions'])*3
                return render_template('quizpage.html',
                                    surname = surname,
                                    userid = user,
                                    ques_data = ques_data,
                                    total_questions=total_questions,
                                    current_index = session['current_index'],
                                    error = error,
                                    ans = ans)
    else:
        return redirect(url_for('login'))

@app.route('/pendingtest', methods=['POST'])
def pendingtest():
    if request.method == 'POST':
        if request.form['contTest'] == 'contTest':
            temp_ques_data = {}
            session['topics'] = list(User_curr_score.find_one({'emailid': session['emailid']})['questions'].keys())
            for key, value in User_curr_score.find_one({'emailid': session['emailid']})['questions'].items():
                temp_ques_data[key] = [int(list(v.keys())[0]) for v in value]
            session['ques_data'] = temp_ques_data
            session['current_index'] = 0
            return redirect(url_for('quizpage'))
        elif request.form['contTest'] == 'quittest':
            #Update the last question...
            new_data = User_curr_score.find_one({'emailid': session['emailid']})['questions']
            time_taken = (datetime.datetime.now() - User_curr_score.find_one({'emailid': session['emailid']})['start_time']).total_seconds()
            User_curr_score.delete_one({'emailid': session['emailid']})
            # Get score
            score = 0
            for topic, user_inp in new_data.items():
                for i in user_inp:
                    for q_no, user_ans in i.items():
                        if user_ans == q_db.find_one({'category': topic, 'q_no': int(q_no)})['answer']:
                            score += 1

            User_score_data.update_one(filter={'emailid': session['emailid']}, update={'$set': {f'test_data.{len(User_score_data.find_one({'emailid':session['emailid']})['test_data'])-1}': new_data,
                                                                                                        f'time_taken.{len(User_score_data.find_one({'emailid':session['emailid']})['time_taken'])-1}': time_taken,
                                                                                                        f'scores.{len(User_score_data.find_one({'emailid':session['emailid']})['scores'])-1}': score}})
            return redirect(url_for('userpage', message='Test submitted without completion.'))

@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("surname", None)
    session.pop("ques_data", None)
    session.pop("current_index", None)
    session.pop("topics", None)
    session.pop("emailid", None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')