'''
Uploads all the possible links of geeksforgeeks on the database by iterating through them.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
file = open('mongo_url.txt')
mongo_url, sk = file.readlines()
mongo_url = mongo_url.strip()
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydata"
client = MongoClient(mongo_url)
file.close()
db = client['MCQ-tool']
collection = db['GFG_links']

@app.route('/add_data', methods=['POST'])
def add_data(data):
    collection.insert_one(data)
    return jsonify(message="Successfully added data record"), 201

@app.route('/delete_all_records', methods=['POST'])
def delete_all_records():
    result = collection.delete_many({})
    if result.deleted_count > 0:
        return jsonify(message='All records deleted successfully.'), 200
    else:
        return jsonify(message='No records found to delete.'), 404

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--start-maximized')  # Maximize window to ensure links are clickable
chrome_options.add_argument('--headless')  # Optional: Run in headless mode
chrome_options.add_argument('--log-level=3') #Suppress logging of info
chrome_options.add_argument('--log-level=2') #Suppress logging of errors

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_sub_links(url, sublink_list):
    driver.get(url)
    try:
        more_pages = driver.find_elements(By.CLASS_NAME, 'QuizPagination_singlePage_head__5grOk')
        for pages in more_pages:
            page_link = pages.get_attribute('href')
            sublink_list.append(page_link)
        return sublink_list
    except(Exception):
        return sublink_list

def scrape_and_store_links():
    driver.get('https://www.geeksforgeeks.org/quiz-corner-gq/')
    time.sleep(5)

    all_questions = driver.find_element(By.CLASS_NAME, 'page_content')
    left_div_tags = all_questions.find_elements(By.XPATH, '//div[@style="width: 50%;float: left"]')
    right_div_tags = all_questions.find_elements(By.XPATH, '//div[@style="width: 50%;float: right"]')
    
    links_list = []
    for left_div_tag in left_div_tags:
        left_a_tags = left_div_tag.find_elements(By.TAG_NAME, 'a')
        for left_a_tag in left_a_tags:
            left_url = left_a_tag.get_attribute('href')
            links_list.append(left_url)
    
    
    for right_div_tag in right_div_tags:
        right_a_tags = right_div_tag.find_elements(By.TAG_NAME, 'a')
        for right_a_tag in right_a_tags:
            right_url = right_a_tag.get_attribute('href')
            links_list.append(right_url)
    
    l = len(links_list)
    for i in range(l):
        links_list = get_sub_links(links_list[i], links_list)
    
    with app.app_context():
        delete_all_records()
        links_dict = {}
        for i in range(len(links_list)):
            links_dict[str(i+1)] = links_list[i]
        add_data(links_dict)
        print('*'*100)
        print('Done.....')
    
    print("Done uploading.")
    driver.quit()

if __name__ == '__main__':
    with app.app_context():
        scrape_and_store_links()
    app.run(debug=True)
