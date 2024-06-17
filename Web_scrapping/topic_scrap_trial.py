from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from pymongo import MongoClient

# List of links to process
links = [
    'https://www.freetimelearning.com/online-quiz/dotnet-mcq.php',
    'https://www.freetimelearning.com/online-quiz/python-quiz.php',
    'https://www.freetimelearning.com/online-quiz/react-js-quiz.php',
    'https://www.freetimelearning.com/online-quiz/javascript-quiz.php',
    # 'https://www.freetimelearning.com/online-quiz/node-js-quiz.php',
    # 'https://www.freetimelearning.com/online-quiz/flask-quiz.php',
    # 'https://www.freetimelearning.com/online-quiz/mongodb-quiz.php',
    # 'https://www.freetimelearning.com/online-quiz/mysql-quiz.php',
    # 'https://www.freetimelearning.com/online-quiz/postgresql-quiz.php'
]

# MongoDB client setup
client = MongoClient('mongodb+srv://hemangmehta1703:hemang@mcq-tool.orytooa.mongodb.net/?retryWrites=true&w=majority&appName=MCQ-tool')
db = client['MCQ-tool']
questions_database = db['Topic_wise_questions']

# Chrome options setup for headless browsing
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--log-level=3')

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to extract and print questions and answers
def extract_questions_and_answers(url):
    driver.get(url)
    driver.implicitly_wait(3)
    driver.execute_script("document.querySelectorAll('.show_gk_ans').forEach(el => el.style.display = 'block');")
    time.sleep(3)

    ques_card = driver.find_elements(By.CSS_SELECTOR, 'div.quiz-question')
    ques_ans = driver.find_elements(By.CSS_SELECTOR, 'div.quiz-question-answer')
    question_list = []
    category = url.split('/')[4].split('.')[0].split('-')[:-1][0]
    for j in range(len(ques_card)):
        a = ques_card[j].find_element(By.CSS_SELECTOR, 'div.question')
        q_no = int(a.find_element(By.CLASS_NAME, 'question-left').text.split(' ')[0])
        try:
            question = a.find_element(By.CSS_SELECTOR, '.question-right a').text
        except Exception:
            try:
                question = a.find_element(By.CSS_SELECTOR, 'div.question-right.quiz_ta_question_color').text
            except:
                try:
                    question = a.find_element(By.CSS_SELECTOR, 'div.question-right').text
                except:
                    question = ''

        print(f"{q_no}")

        option_card = ques_ans[j].find_elements(By.CSS_SELECTOR, '.quiz-ans-margin')
        ans_container = ques_ans[j].find_element(By.CLASS_NAME, 'show_gk_ans')
        p_class = ans_container.find_element(By.CLASS_NAME, 'bold')
        span_class = p_class.find_element(By.CLASS_NAME, 'ans-text-color').text
        try:
                or_ans = ans_container.find_element(By.TAG_NAME, 'div').text
                span_class = or_ans if len(or_ans)>len(span_class) else span_class
        except:
            continue
        # print("Options:")
        option_text = []
        for i, option in enumerate(option_card, start=1):
            if option.text != '':
                option_text.append(option.text.strip())
                # print(f"{i}. {option.text.strip()}")

        # print(f"Correct answer: {span_class}")
        # print()
        question_list.append({'category': category, 'question': question, 'options': option_text, 'answer':span_class, 'q_no': q_no})
        
    return question_list

def add_to_database(question_list, link):
    for q in question_list:
        # print(f"ieufhweiroh twohoihg ---> {q}")
        questions_database.insert_one(q)
    print("Data of {} successfully added to mongodb.".format(link))

# Process each link in the list
# for link in links:
#     print(f"Processing: {link}")
#     question_list = extract_questions_and_answers(link)
#     add_to_database(question_list, link)
#     print("-" * 80)
#     break
link = links[3]
question_list = extract_questions_and_answers(link)
for i in question_list:
    print(i)
    print()
# add_to_database(question_list, link)
# Close the WebDriver
driver.quit()
