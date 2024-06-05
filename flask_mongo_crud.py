from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

app=Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydata"
file = open('mongo_url.txt')
mongo_url, sk = file.readlines()
mongo_url = mongo_url.strip()
client = MongoClient(mongo_url)
file.close()

db = client['MCQ-tool']
collection = db['data']

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/userpage')
def user():
    return render_template('userpage.html')

@app.route('/delete_all_records', methods=['POST'])
def delete_all_records():
    result = collection.delete_many({})
    if result.deleted_count > 0:
        return jsonify(message='All records deleted successfully.'), 200
    else:
        return jsonify(message='No records found to delete.'), 404

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    print(data)
    collection.insert_one(data)
    return jsonify(message="Successfully added data record"), 201


@app.route('/printdata', methods=['GET'])
def read_data():
    data = list(collection.find({}))
    return render_template('printdata.html', data=data)

@app.route('/update_data', methods=['GET', 'POST'])
def update_data():
    name = request.form.get('name')
    new_password = request.form.get('new_password')
    collection.update_one({'name': name}, {'$set': {'password': new_password}})
    return render_template('updatedata.html')

if __name__ == '__main__':
    app.run(debug=True)