def scrape_questions(numlinks):
    from Web_scrapping import gfg_single_quiz_questions
    from pymongo import MongoClient

    file = open('mongo_url.txt')
    mongo_url, sk = file.readlines()
    mongo_url = mongo_url.strip()
    client = MongoClient(mongo_url)
    file.close()

    db = client['MCQ-tool']
    quiz_links = db['GFG_links']
    questions_database = db['Questions_database']

    def add_data(new_gfg_ques):
        for i in new_gfg_ques:
            questions_database.insert_one(i)
        print("Data successfully added to mongodb.")

    links = list(quiz_links.find({}))
    gfg_ques = list(questions_database.find({}))


    counter = 0
    file = open('Web_scrapping\counter.txt', 'r+')
    counter = int(file.read())

    final_counter = int(numlinks)+counter
    print(f'Counter will go from {counter} to {final_counter}\n\n')

    while counter<final_counter:
        for key, value in links[0].items():
            if key == str(counter):
                if value != None:
                    print(key, value)
                    new_gfg_ques = gfg_single_quiz_questions.get_questions(value, gfg_ques)
        counter += 1

    print(f"New Counter = {counter}")
    file.seek(0)
    file.write(str(counter))
    questions_database.delete_many({})
    add_data(new_gfg_ques)
    file.close()

    return True