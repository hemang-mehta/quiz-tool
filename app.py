from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://hemangmehta1703:hemang@mcq-tool.orytooa.mongodb.net/?retryWrites=true&w=majority&appName=MCQ-tool')

collection = client['MCQ-tool']
user_data = collection['User_data']

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydata"

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    user_data.insert_one(data)
    return jsonify(message="Successfully added data record"), 201

#Hello world

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/userpage')
def user_page():
    return render_template('userpage.html')

if __name__ == "__main__":
    app.run(debug=True)