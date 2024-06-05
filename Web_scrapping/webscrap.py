from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--start-maximized')  # Maximize window to ensure links are clickable
chrome_options.add_argument('--headless')  # Optional: Run in headless mode

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# Open the main page

driver.get("https://www.geeksforgeeks.org/quizzes/c-language-2-gq/operators-gq/")
time.sleep(3)  # Wait for the page to load

more_pages = driver.find_elements(By.CLASS_NAME, 'QuizPagination_singlePage_head__5grOk')
for pages in more_pages:
    page_link = pages.get_attribute('href')
    print(page_link)
    
    
"""

driver.get("https://www.geeksforgeeks.org/questions/c-c-quiz-101-question-1/")
ques = driver.find_element(By.CLASS_NAME, 'QuizQuestionDiscuss_quizQuestionDiscussMainContainer_notGfgTabs__iShFT')
q = ques.find_element(By.XPATH, './div')
print(q.text.split('\n')[-1])
"""
# links = driver.find_element(By.CLASS_NAME, 'QuizQuestionCard_quizCard__tagCollection__discussIt__P4q4G')
# x = links.find_element(By.TAG_NAME, 'a')
# y = x.get_attribute('href')
# driver.get('https://www.geeksforgeeks.org/questions/c-c-quiz-101-question-3/')
# #opened link from discuss it

# question = driver.find_element(By.CLASS_NAME, 'QuizQuestionDiscuss_quizQuestionDiscussMainContainer_notGfgTabs__iShFT')
# print(question.text.split('\n')[0])
# link_2 = driver.find_element(By.CLASS_NAME, 'QuizQuestionDiscuss_quizQuestionDiscussMainContainer_questionExplanationContainer__yLYZ3')
# print(link_2.text)
# print('*'*20)
# print(link_2.find_element(By.TAG_NAME, 'b').text)

# qanda = driver.find_element(By.CLASS_NAME, 'QuizQuestionDiscuss_quizQuestionDiscussMainContainer__xLPUU')
# x_1 = qanda.find_element(By.CLASS_NAME, 'QuizQuestionDiscuss_quizQuestionDiscussMainContainer_notGfgTabs__iShFT')
# print(x_1.text)



driver.quit()