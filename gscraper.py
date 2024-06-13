from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import time

# Initialize the driver
cdp = "/usr/bin/geckodriver"
service = Service(executable_path=cdp)
driver = webdriver.Firefox(service=service)

link = input("Enter the GitHub link you want to scrape: ")
global prompt 
prompt = input("Enter the keyword you want to search for:")
driver.get(f'{link}/?tab=repositories')
time.sleep(2)
res = driver.find_elements(By.XPATH, "//a[@itemprop='name codeRepository']")
time.sleep(2)

repo_list = []
repo_links = []

def going_for_raw(file_link):
    time.sleep(15)
    driver.get(file_link)
    try:
        raw = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[@data-testid='raw-button']")))
        #raw = driver.find_element(By.XPATH, "//*[@data-testid='raw-button']")
        #print(file_link)
        time.sleep(15)
        raw.click()
        html = driver.page_source
        html = f'{html}'
        if prompt in html: 
            print("found keyword")
            print(file_link)
    except Exception as e: 
        print(f'Error in going for raw: {e}')
        


# Function to process file links

# Recursive function to process folder contents
def cycle3(folder_link, folder_name, repo_link):
    driver.get(folder_link)
    time.sleep(2)
    
    res = driver.find_elements(By.CLASS_NAME, "react-directory-truncate")
    file_in_folder_list = []
    for k in res: 
        if k.text != '':
            file_in_folder_list.append(k.text)

    file_links = []
    folder_links = []

    for k in file_in_folder_list:
        branch_element = driver.find_element(By.XPATH, "//span[@class='Text-sc-17v1xeu-0 bOMzPg']")
        branch = branch_element.text[1:]  # Remove the first character

        if "." in k and not k.startswith('.') and "png" not in k and "jpg" not in k and "jpeg" not in k and "gif" not in k and "pdf" not in k:
            add = f'{repo_link}/blob/{branch}/{folder_name}/{k}'
            file_links.append(add)
            going_for_raw(add)
        elif not "." in k or k.startswith('.'):
            add = f'{folder_link}/{k}'
            folder_links.append(add)
            k_full_path = f'{folder_name}/{k}'
            cycle3(add, k_full_path, repo_link)
        else: 
            continue

# Function to process repositories
def cycle(repo_link):
    driver.get(repo_link)
    time.sleep(2)
    
    res = driver.find_elements(By.CLASS_NAME, "react-directory-truncate")
    file_list = []
    
    for i in res: 
        if i.text!='':
            file_list.append(i.text)
          
    file_links = []
    folder_links = []
     
    for i in file_list:
        branch_element = driver.find_element(By.XPATH, "//span[@class='Text-sc-17v1xeu-0 bOMzPg']")
        branch = branch_element.text[1:]  # Remove the first character
        
        if "." in i and not i.startswith('.') and "png" not in i and "jpg" not in i and "jpeg" not in i and "gif" not in i and "pdf" not in i:
            add = f'{repo_link}/blob/{branch}/{i}'
            file_links.append(add)
            going_for_raw(add)
        elif not "." in i or i.startswith('.'):
            add = f'{repo_link}/tree/{branch}/{i}'
            folder_links.append(add)
            cycle3(add, i,repo_link)
        else: 
            continue

# Extract repository names and links
for i in res:
    #print(i.text)
    repo_list.append(i.text)

for repo_name in repo_list:
    add = f'{link}/{repo_name}'
    repo_links.append(add)
    cycle(add)

driver.quit()

