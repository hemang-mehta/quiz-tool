from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

from pymongo import MongoClient

links = [
    'https://www.freetimelearning.com/online-quiz/dotnet-mcq.php',
    'https://www.freetimelearning.com/online-quiz/python-quiz.php',
    'https://www.freetimelearning.com/online-quiz/react-js-quiz.php',
    'https://www.freetimelearning.com/online-quiz/javascript-quiz.php',
    'https://www.freetimelearning.com/online-quiz/node-js-quiz.php',
    'https://www.freetimelearning.com/online-quiz/flask-quiz.php',
    'https://www.freetimelearning.com/online-quiz/mongodb-quiz.php',
    'https://www.freetimelearning.com/online-quiz/mysql-quiz.php',
    'https://www.freetimelearning.com/online-quiz/postgresql-quiz.php'
]

client = MongoClient('mongodb+srv://hemangmehta1703:hemang@mcq-tool.orytooa.mongodb.net/?retryWrites=true&w=majority&appName=MCQ-tool')
db = client['MCQ-tool']
questions_database = db['Topic_wise_questions']

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--log-level=3')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.freetimelearning.com/online-quiz/dotnet-mcq.php')
driver.implicitly_wait(3)

# question_element = driver.find_elements(By.CSS_SELECTOR, '.quiz-question .question-right a')
# question_element1 = driver.find_elements(By.CSS_SELECTOR, '.quiz-question .question-right.quiz_ta_question_color')

# questions = [element.text for element in question_element if element.text != '']
# for i in question_element1:
#     questions.append(i.text)
# for idx, question in enumerate(questions, start=1):
#     print(f"Question {idx}: {question}")



# q_cards = driver.find_elements(By.TAG_NAME, 'div')
# for q in q_cards:
#     q_question = q.find_element(By.CLASS_NAME, 'quiz-question')
#     q_row = q.find_element(By.CLASS_NAME, 'row')
#     q_no = q_row.find_element(By.CLASS_NAME, 'question-left').text
#     print(q_no)

ques_card = driver.find_elements(By.CSS_SELECTOR, 'div.quiz-question')
ques_ans = driver.find_elements(By.CSS_SELECTOR, 'div.quiz-question-answer')
for j in range(len(ques_card)):
    a = ques_card[j].find_element(By.CSS_SELECTOR, 'div.question')
    q_no = a.find_element(By.CLASS_NAME, 'question-left')
    question = a.find_element(By.CSS_SELECTOR, '.question-right a').text
    print(q_no.text[:2], end=' ')
    if question=='':
        try:
            question = a.find_element(By.CSS_SELECTOR, 'div.question-right.quiz_ta_question_color').text
        except Exception:
            question = ''



    option_card = ques_ans[j].find_elements(By.CSS_SELECTOR, 'div.quiz-ans-margin')
    ans_container = ques_ans[j].find_element(By.CSS_SELECTOR, 'div.show_gk_ans.p10_0')
    correct_answer = ans_container.find_element(By.CSS_SELECTOR, 'span.ans-text-color').getText()
    # correct_ans = ans_container.find_element(By.CSS_SELECTOR, 'p.bold').text
    # print(question)
    # print('Options -> ')
    # for i in option_card:
    #     print(i.text)
    print('Correct answer: {}'.format(correct_answer))
    print()


driver.quit()