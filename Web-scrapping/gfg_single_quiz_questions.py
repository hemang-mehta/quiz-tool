'''
Returns the questions from the current website.
Along with the question, it returns code, options, correct answer.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re

def get_questions(main_page, gfg):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Optional: Run in headless mode
    chrome_options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
    chrome_options.add_argument('--log-level=3') #Suppress logging of info

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    def sanitize_url(url):
        """Remove repeated forward slashes from the URL."""
        return re.sub(r'(?<!:)//+', '/', url)
    #main page
    driver.get(main_page)
    time.sleep(3)
    # Get the tags for the Discuss it links
    links = driver.find_elements(By.CLASS_NAME, 'QuizQuestionCard_quizCard__tagCollection__discussIt__P4q4G')
    # Get the urls from those links
    hrefs = [sanitize_url(link.find_element(By.TAG_NAME, 'a').get_attribute('href')) for link in links]
    
    q_no = 1
    for href in hrefs:
        try:
            driver.get(href)
            try:
                ques = driver.find_element(By.CLASS_NAME, 'QuizQuestionDiscuss_quizQuestionDiscussMainContainer_notGfgTabs__iShFT')
                q = ques.find_element(By.XPATH, './div')
                question = q.text.split('\n')[0]
                qst = q.text.split('\n')[-1]
                if len(qst)>len(question): question = qst
                code = driver.find_element(By.CLASS_NAME, 'highlight')
                code_snippet = code.text
            except(Exception):
                comp_ques = driver.find_elements(By.CLASS_NAME, 'QuizQuestionDiscuss_quizQuestionDiscussMainContainer_questionsAndOptions__2TYvt')
                q = comp_ques[0].find_element(By.XPATH, './div')
                question = q.text
                code_snippet = None

            Answer = driver.find_element(By.CLASS_NAME, 'QuizQuestionDiscuss_quizQuestionDiscussMainContainer_questionExplanationContainer__yLYZ3')
            Correct_option = Answer.text.split(' ')[1][1]

            options = driver.find_elements(By.XPATH, "//div[@style='display:flex;gap:10px']")
            options_list = []
            for option in options:
                op = option.find_element(By.TAG_NAME, 'div')
                options_list.append(op.text)

            gfg[question] = {'options':options_list, 'correct_ans': Correct_option, 'code': code_snippet}
        except Exception as e:
            print('*'*100)
            print(f"Exception {Exception} occured for quesiton {q_no}.")
        finally:
            q_no += 1
    driver.quit()
    return gfg

# diction = {}
# x = get_questions('https://www.geeksforgeeks.org/quizzes/c-language-2-gq/operators-gq/', diction)
# print(x)