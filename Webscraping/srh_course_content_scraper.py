from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

output_folder = "./outputs"
Path(output_folder).mkdir(parents=True, exist_ok=True)

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
waiter = WebDriverWait(driver, 10)

course_pages = [
                'https://www.srh-hochschule-heidelberg.de/en/master/information-technology/',
                'https://www.srh-hochschule-heidelberg.de/en/master/international-business-and-engineering/',
                'https://www.srh-hochschule-heidelberg.de/en/master/water-technology/',
                'https://www.srh-hochschule-heidelberg.de/en/master/blockchain-technology/',
                'https://www.srh-hochschule-heidelberg.de/en/master/artificial-intelligence/',
                'https://www.srh-hochschule-heidelberg.de/en/master/architecture/',
                'https://www.srh-hochschule-heidelberg.de/en/master/applied-computer-science/',
                'https://www.srh-hochschule-heidelberg.de/en/master/applied-data-science-and-analytics/',
                'https://www.srh-hochschule-heidelberg.de/en/master/music-therapy/',
                'https://www.srh-hochschule-heidelberg.de/en/master/dance-movement-therapy/',
                'https://www.srh-hochschule-heidelberg.de/en/master/global-business-and-leadership/',
                'https://www.srh-hochschule-heidelberg.de/en/master/international-management-and-leadership/'
                ]

course_content_df = pd.DataFrame()

def get_course_name():
    try:
        return driver.find_element(By.CSS_SELECTOR, 'h1.b_headline').text
    except NoSuchElementException:
        try:
            return driver.find_element(By.CSS_SELECTOR, 'span.b_headline--color-primary').text
        except NoSuchElementException:
            print('course name not found')
            return ''
    
def get_all_course_tags():
    return _get_course_tags() + ', ' + _get_additional_tags()

def _get_additional_tags():
    try:
        return ', '.join(driver.find_element(By.CSS_SELECTOR, 'div.b_st-content__list').text.split('\n'))
    except NoSuchElementException:
        print('additional tags not found')
        return ''

def _get_course_tags():
    try:
        return ', '.join(driver.find_element(By.CSS_SELECTOR, 'ul.b_tag-list').text.split('\n'))
    except NoSuchElementException:
        print('course tags not found')
        return ''
    
def get_course_description():
    try:
        return driver.find_element(By.CSS_SELECTOR, 'div.b_st-content__main-content > div:nth-child(1)').text
    except NoSuchElementException:
        print('course description not found')
        return ''

def get_all_course_content():
    return _get_course_content() + ' ' + _get_additional_course_content()

def _get_course_content():
    try:
        element = driver.find_element(By.CSS_SELECTOR, 'section.b_cm_text:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')
        ActionChains(driver).move_to_element(element).perform()
        waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'section.b_cm_text:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')))
        return element.text.replace('\n', ' ')
    except NoSuchElementException:
        print('course content not found')
        return ''
    except TimeoutException:
        print('course content not found')
        return ''

def _get_additional_course_content():
    try:
        ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'body > main > div:nth-child(3) > section.b_cm_text.bJS_cm_text.b_cm_text--spacing-top.b_cm_text--bg-grey')).perform()
        waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#uid-accordion-button-content > span:nth-child(2) > svg:nth-child(1)')))
        ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR, '#uid-accordion-button-content > span:nth-child(2) > svg:nth-child(1)')).perform()
        waiter.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="uid-accordion-panel-content"]/div/div')))
        return driver.find_element(By.XPATH, '//*[@id="uid-accordion-panel-content"]/div/div').text.replace('\n', ' ')
    except NoSuchElementException:
        try:
            ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, '#uid-accordion-button-content > span.b_icon.b_icon--l')).perform()
            waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#uid-accordion-button-content > span:nth-child(2) > svg:nth-child(1)')))
            ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR, '#uid-accordion-button-content > span:nth-child(2) > svg:nth-child(1)')).perform()
            waiter.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="uid-accordion-panel-content"]/div/div')))
            return driver.find_element(By.XPATH, '//*[@id="uid-accordion-panel-content"]/div/div').text.replace('\n', ' ')
        except NoSuchElementException:
            print('additional content not found')
            return ''
        except TimeoutException:
            print('additional content not found')
            return ''
    except TimeoutException:
            try:
                ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, '#uid-accordion-button-content > span.b_icon.b_icon--l')).perform()
                waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#uid-accordion-button-content > span:nth-child(2) > svg:nth-child(1)')))
                ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR, '#uid-accordion-button-content > span:nth-child(2) > svg:nth-child(1)')).perform()
                waiter.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="uid-accordion-panel-content"]/div/div')))
                return driver.find_element(By.XPATH, '//*[@id="uid-accordion-panel-content"]/div/div').text.replace('\n', ' ')
            except NoSuchElementException:
                print('additional content not found')
                return ''
            except TimeoutException:
                print('additional content prospects not found')
                return ''

def get_all_career_prospects():
    return _get_career_prospects() + ' ' + _get_additional_career_prospects()

def _get_career_prospects():
    try:
        element = driver.find_element(By.CSS_SELECTOR, 'section.b_cm_text--bg-grey:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')
        ActionChains(driver).move_to_element(element).perform()
        waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'section.b_cm_text--bg-grey:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')))
        return element.text.replace('\n', ' ')
    except NoSuchElementException:
        print('career prospects not found')
        return ''
    except TimeoutException:
        print('career prospects not found')
        return ''
    
def _get_additional_career_prospects():
    try:
        ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'section.b_tm_image:nth-child(5)')).perform()
        waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#uid-accordion-button-perspectives > span:nth-child(2) > svg:nth-child(1)')))
        ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR, '#uid-accordion-button-perspectives > span:nth-child(2) > svg:nth-child(1)')).perform()
        waiter.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="uid-accordion-panel-perspectives"]/div/div')))
        return driver.find_element(By.XPATH, '//*[@id="uid-accordion-panel-perspectives"]/div/div').text.replace('\n', ' ')
    except NoSuchElementException:
        try:
            ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'section.b_cm_text--bg-grey:nth-child(3)')).perform()
            waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#uid-accordion-button-perspectives > span:nth-child(2) > svg:nth-child(1)')))
            ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR, '#uid-accordion-button-perspectives > span:nth-child(2) > svg:nth-child(1)')).perform()
            waiter.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="uid-accordion-panel-perspectives"]/div/div')))
            return driver.find_element(By.XPATH, '//*[@id="uid-accordion-panel-perspectives"]/div/div').text.replace('\n', ' ')
        except NoSuchElementException:
            print('additional career prospects not found')
            return ''
        except TimeoutException:
            print('additional career prospects not found')
            return ''
    except TimeoutException:
        try:
            ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'section.b_cm_text--bg-grey:nth-child(3)')).perform()
            waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#uid-accordion-button-perspectives > span:nth-child(2) > svg:nth-child(1)'))).click().perform()
            waiter.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="uid-accordion-panel-perspectives"]/div/div')))
            return driver.find_element(By.XPATH, '//*[@id="uid-accordion-panel-perspectives"]/div/div').text.replace('\n', ' ')
        except NoSuchElementException:
            print('additional career prospects not found')
            return ''
        except TimeoutException:
            print('additional career prospects not found')
            return ''

def get_curriculum():
    try:
        ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, '.b_lm_curriculum__curriculum')).perform()
        waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.b_lm_curriculum__curriculum')))
        parent_div = driver.find_element(By.CSS_SELECTOR, '.b_lm_curriculum__curriculum')
        buttons = parent_div.find_elements(By.TAG_NAME, 'button')
        sections = parent_div.find_elements(By.TAG_NAME, 'section')
        all_curriculum = ''
        for button, section in zip(buttons, sections):
            ActionChains(driver).move_to_element(button).perform()
            button.click()
            sem = section.find_element(By.CSS_SELECTOR, 'span.b_lm_curriculum__panel-title').text + ' '
            items = section.find_elements(By.TAG_NAME, 'li')
            for item in items:
                sem += item.text.replace('\n', ' ') + ' ECTS '
            all_curriculum += sem
        return all_curriculum
    except NoSuchElementException:
        print('course curriculum not found')
        return ''
    except TimeoutException:
        print('course curriculum not found')
        return ''

def get_requirements():
    try:
        section = driver.find_element(By.CSS_SELECTOR, 'body > main > div:nth-child(5) > section:nth-child(3)')
        ActionChains(driver).move_to_element(section).perform()
        waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > main > div:nth-child(5) > section:nth-child(3) > div > div > div.b_cm_text__main')))
        return section.find_element(By.CSS_SELECTOR, 'body > main > div:nth-child(5) > section:nth-child(3) > div > div > div.b_cm_text__main').text.replace('\n', ' ')
    except NoSuchElementException:
        try:
            section = driver.find_element(By.CSS_SELECTOR, 'body > main > div:nth-child(6) > section:nth-child(3)')
            ActionChains(driver).move_to_element(section).perform()
            waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > main > div:nth-child(6) > section:nth-child(3) > div > div > div.b_cm_text__main')))
            return section.find_element(By.CSS_SELECTOR, 'body > main > div:nth-child(6) > section:nth-child(3) > div > div > div.b_cm_text__main').text.replace('\n', ' ')
        except NoSuchElementException:
            print('requirements not found')
            return ''
        except TimeoutException:
            print('requirements prospects not found')
            return ''
    except TimeoutException:
        try:
            section = driver.find_element(By.CSS_SELECTOR, 'body > main > div:nth-child(6) > section:nth-child(3)')
            ActionChains(driver).move_to_element(section).perform()
            waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > main > div:nth-child(6) > section:nth-child(3) > div > div > div.b_cm_text__main')))
            return section.find_element(By.CSS_SELECTOR, 'body > main > div:nth-child(6) > section:nth-child(3) > div > div > div.b_cm_text__main').text.replace('\n', ' ')
        except NoSuchElementException:
            print('requirements not found')
            return ''
        except TimeoutException:
            print('requirements prospects not found')
            return ''

def get_fees():
    try:
        section = driver.find_element(By.CSS_SELECTOR, 'section.b_cm_text:nth-child(5)')
        ActionChains(driver).move_to_element(section).perform()
        waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'section.b_cm_text:nth-child(5) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)')))
        return section.find_element(By.CSS_SELECTOR, 'section.b_cm_text:nth-child(5) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)').text.replace('\n', ' ')
    except NoSuchElementException:
        print('tuition fees not found')
        return ''
    except TimeoutException:
        print('tuition fees not found')
        return ''

def get_process():
    try:
        section = driver.find_element(By.CSS_SELECTOR, 'section.b_cm_text:nth-child(7)')
        ActionChains(driver).move_to_element(section).perform()
        waiter.until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[3]/section[4]/div/div/div[2]')))
        return section.find_element(By.XPATH, '/html/body/main/div[3]/section[4]/div/div/div[2]').text.replace('\n', ' ')
    except NoSuchElementException:
        try:
            section = driver.find_element(By.CSS_SELECTOR, 'section.b_cm_text:nth-child(7)')
            ActionChains(driver).move_to_element(section).perform()
            waiter.until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[4]/section[4]/div/div/div[2]')))
            return section.find_element(By.XPATH, '/html/body/main/div[4]/section[4]/div/div/div[2]').text.replace('\n', ' ')
        except NoSuchElementException:
            print('application process and deadlines not found')
            return ''
        except TimeoutException:
            print('application process and deadlines not found')
            return ''
    except TimeoutException:
        try:
            section = driver.find_element(By.CSS_SELECTOR, 'section.b_cm_text:nth-child(7)')
            ActionChains(driver).move_to_element(section).perform()
            waiter.until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[4]/section[4]/div/div/div[2]')))
            return section.find_element(By.XPATH, '/html/body/main/div[4]/section[4]/div/div/div[2]').text.replace('\n', ' ')
        except NoSuchElementException:
            print('application process and deadlines not found')
            return ''
        except TimeoutException:
            print('application process and deadlines not found')
            return ''

for i, c in enumerate(course_pages):
    driver.get(c)
    time.sleep(2)
    course_content_df.loc[i, 'Name'] = get_course_name()
    course_content_df.loc[i, 'Tags'] = get_all_course_tags()
    course_content_df.loc[i, 'Description'] = get_course_description()
    course_content_df.loc[i, 'Content'] = get_all_course_content()
    course_content_df.loc[i, 'Career Prospects'] = get_all_career_prospects()
    course_content_df.loc[i, 'Curriculum'] = get_curriculum()
    course_content_df.loc[i, 'Requirements'] = get_requirements()
    course_content_df.loc[i, 'Tuition Fees'] = get_fees()
    course_content_df.loc[i, 'Application Process and Deadlines'] = get_process()

driver.close()
course_content_df.to_csv(output_folder + '/' + 'srh_masters_course_content.csv', index=False)