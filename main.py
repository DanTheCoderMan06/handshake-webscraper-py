import os
from dotenv import load_dotenv
import time
import threading
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

global driver
global running 
global jobs 

def jobs_loop():
    global running
    global jobs 
    jobs = []
    while(running):
        pane = get_pane()
        next_button = get_next()
        jobDivs = get_jobs(get_div_Container(pane))
        time.sleep(10)
        for job in jobDivs:
            jobs.append(get_info(job))
        next_button.click()
        time.sleep(15)

def get_pane():
    global driver 
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-hook='search-results']"))
    )
    return element

def get_next():
    global driver 
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-hook='search-pagination-next']"))
    )
    return element

def is_done():
    global driver 
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-hook='search-pagination-next']"))
    )
    parentDiv = element.find_element(By.XPATH,"..")
    counterDiv = parentDiv.find_element(By.TAG_NAME,"div")
    counterText = counterDiv.get_attribute("innerHTML")
def get_div_Container(container):
    global driver 
    element = WebDriverWait(container, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[tabindex=\"-1\"]"))
    )
    return element

def get_jobs(container):
    global driver 
    children = container.find_elements(By.XPATH, "./*")
    return children

def get_info(container):
    global driver 
    info = {
        "image" : "",
        "title" : "",
        "company" : "",
        "link" : "",
        "extraInfos" : [],
    }

    title = container.find_element(By.TAG_NAME, "h3")
    img_elements = container.find_element(By.TAG_NAME, "img")

    companyInfoCardContainer = img_elements.find_element(By.XPATH, "..")

    for divInfo in companyInfoCardContainer.find_elements(By.TAG_NAME,"div"):
        inner_html = divInfo.get_attribute("innerHTML")
        soup = BeautifulSoup(inner_html, "html.parser")
        text_content = soup.get_text(strip=True)
        if text_content:
            info["company"] += text_content + " "

    seperators = container.find_elements(By.XPATH, ".//*[contains(text(), '∙')]")

    info["title"] = title.text  
    info["image"] = img_elements.get_attribute("src")
    info["link"] = container.find_element(By.XPATH,".//*[@data-hook='jobs-card']").get_attribute("href")

    infoContainers = set()
    
    for infoContainer  in seperators:
        try:
            parent_element = infoContainer.find_element(By.XPATH, "..")
            inner_html = parent_element.get_attribute("innerHTML")
            soup = BeautifulSoup(inner_html, "html.parser")
            text_content = soup.get_text(strip=True)
            if text_content:
                infoContainers.add(text_content)  
        except:
            print("FATAL INFO FETCH FAILURE!")
            continue

    info["extraInfos"] = list(infoContainers)

    print("Scraped Job: ")
    print(info)
    return(info)

def write_csv():
    global jobs

    max_extra_infos = max(len(entry["extraInfos"]) for entry in jobs)
    headers = ["Image", "Company", "Job Title", "Link"] + [f"ExtraInfo {i+1}" for i in range(max_extra_infos)]

    with open(os.getenv("OUTPUT_CSV"), mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers) 

        for entry in jobs:
            image_html = f'=IMAGE("{entry["image"]}", 4, 50, 50)' 
            link_html = f'=HYPERLINK("{entry["link"]}", "Link")'
            row = [
                image_html,
                entry["company"],
                entry["title"],
                link_html
            ] + entry["extraInfos"] + [""] * (max_extra_infos - len(entry["extraInfos"]))
            writer.writerow(row)  

def main():
    global driver 
    global running
    running = True
    currentTime = time.time()
    load_dotenv()

    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    driver.get(os.getenv("LOGIN_URL"))

    input("Press Enter when logged in...")

    driver.get(os.getenv("JOBS_URL"))

    jobsThread = threading.Thread(target=jobs_loop)
    jobsThread.start()

    input("Press Enter when finished...")
    running = False
    driver.quit()
    
    write_csv()

    print("COMPLETED WEBSCAPE! TAKING: " + str(time.time() - currentTime))

if __name__ == '__main__':
    main()