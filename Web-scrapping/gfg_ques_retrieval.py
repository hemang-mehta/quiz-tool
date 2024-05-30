import gfg_single_quiz_questions
from pymongo import MongoClient

client = MongoClient('mongodb+srv://hemangmehta1703:hemang@mcq-tool.orytooa.mongodb.net/?retryWrites=true&w=majority&appName=MCQ-tool')

db = client['MCQ-tool']
quiz_links = db['GFG_links']
questions_database = db['GFG_questions_data']

links = list(quiz_links.find({}))
gfg_ques = list(questions_database.find({}))
if gfg_ques == []:
    gfg_ques = [{}]
else:
    if "_id" in gfg_ques[0]:
        del gfg_ques[0]["_id"]

def add_data():
    questions_database.drop()
    questions_database.insert_one(gfg_ques[0])
    print("Data successfully added to mongodb.")

counter = 0
file = open('Web-scrapping\counter.txt', 'r+')
counter = int(file.read())

final_counter = int(input('Enter the number of links to scrap questions.'))+counter
print(f'Counter will go from {counter} to {final_counter}\n\n')

while counter<final_counter:
    for key, value in links[0].items():
        if key == str(counter):
            if value != None:
                print(key, value)
                gfg_ques[0] = gfg_single_quiz_questions.get_questions(value, gfg_ques[0])
    counter += 1

print(f"New Counter = {counter}")
file.seek(0)
file.write(str(counter))
add_data()
file.close()