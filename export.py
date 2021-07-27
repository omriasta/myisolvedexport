from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests
from bs4 import BeautifulSoup
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
from const import USERNAME, PASSWORD, TOKEN, TOKEN_EXPIRATION
from auth import Authentication

''' If Current Token doesn't exist or is expired, run the Authentication to get a new Token'''
if TOKEN == '':
    TOKEN = Authentication()
if TOKEN_EXPIRATION < time.time():
    TOKEN = Authentication()
    



''' Set up the selenium driver '''
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
"download.default_directory": str(os.getcwd()) + "/export/", #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
#"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome 
})

            

driver = webdriver.Chrome(executable_path='chromedriver', options=options)

''' Setup the requests session and start the login process'''
s = requests.Session()
cookies = {
    'iSolvedDeviceToken': TOKEN,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
}

data = {
  'ctl00_ToolkitScriptManager1_HiddenField': '',
  '__EVENTTARGET': '',
  '__EVENTARGUMENT': '',
  'ctl00$NoBot1$NoBot1_NoBotExtender_ClientState': '-333',
  'ctl00$DefaultContent$Login1$UserName': USERNAME,
  'ctl00$DefaultContent$Login1$Button1': 'Continue'
}
s.headers = headers
requests.utils.add_dict_to_cookiejar(s.cookies, cookies)
login_0 = s.get('https://accudata.myisolved.com/UserLogin.aspx')
soup = BeautifulSoup(login_0.content, 'html5lib')
data = {}
for tag in soup.select('input[name^=ctl00]'):
    if tag.get('value'):
        key, value = tag['name'], tag['value']
        data[key] = value
    else:
        key = tag['name']
        data[key] = ''

state = { 
    tag['name']: tag['value'] 
        for tag in soup.select('input[name^=__]')
}
data.update(state)

data['ctl00$NoBot1$NoBot1_NoBotExtender_ClientState'] = '-333'
data['ctl00$DefaultContent$Login1$UserName'] = USERNAME
data['ctl00$DefaultContent$Login1$Button1'] = 'Continue'

login_1 = s.post('https://accudata.myisolved.com/UserLogin.aspx', data=data)

soup = BeautifulSoup(login_1.content, 'html5lib')
data = {}
for tag in soup.select('input[name^=ctl00]'):
    if tag.get('value'):
        key, value = tag['name'], tag['value']
        data[key] = value
    else:
        key = tag['name']
        data[key] = ''

state = { 
    tag['name']: tag['value'] 
        for tag in soup.select('input[name^=__]')
}
data.update(state)
data['ctl00$NoBot1$NoBot1_NoBotExtender_ClientState'] = '-675'
data['ctl00$DefaultContent$Login1$UserName'] = USERNAME
data['ctl00$DefaultContent$Login1$Password'] = PASSWORD
data['ctl00$DefaultContent$Login1$Login'] = 'Login'
data['ctl00_ToolkitScriptManager1_HiddenField'] = ''
data.pop('ctl00$DefaultContent$Login1$Cancel', None)


login_2 = s.post('https://accudata.myisolved.com/UserLogin.aspx', data=data)


soup = BeautifulSoup(login_2.content, 'html5lib')
data = {}
for tag in soup.select('input[name^=ctl00]'):
    if tag.get('value'):
        key, value = tag['name'], tag['value']
        data[key] = value
    else:
        key = tag['name']
        data[key] = ''

state = { 
    tag['name']: tag['value'] 
        for tag in soup.select('input[name^=__]')
}
data.update(state)


receive_cookies = s.post('https://accudata.myisolved.com/default.aspx', data=data)

params = (
    ('legalId', ''),
    ('payGroupId', ''),
    ('orgFieldId', ''),
    ('orgValueId', ''),
    ('payrollStatusId', 'A'),
    ('payTypeId', ''),
    ('searchTerm', ''),
)
''' Get an employee list using the filters in params '''
get_emp_list = s.get('https://accudata.myisolved.com/api/EmployeeListViewApi', params=params)
#print(get_emp_list.text)

''' Navigate to an empty page on the domain in order to inject the cookies into selenium '''
driver.get('https://accudata.myisolved.com/test.html')

for c in [c for c in s.cookies if c.domain == 'accudata.myisolved.com']:
    driver.add_cookie({'name': c.name, 'value': c.value, 'path': c.path,
                            'expires': c.expires, 'domain': c.domain})
                         


''' Cookies are now added and we can proceed to the main page as authenticated user '''

driver.get('https://accudata.myisolved.com/default.aspx')

time.sleep(5)
''' Click in order to get to Employee documents menu option '''
driver.find_element_by_xpath('/html/body/form/div[4]/nav/div[2]/div[2]/div/div/table[7]/tbody/tr/td[2]/a').click()
driver.find_element_by_xpath('//*[@id="ctl00_navigationMenu_Pane_0_content_TreeViewt47"]').click()
time.sleep(5)
''' Find out how many rows are in the Employee grid and select the first '''
rows = driver.find_elements_by_xpath('//*[@id="employeeListGrid"]/div/div/div[6]/div/div/div[1]/div/table/tbody/tr')
row_range = range(1, len(rows))
for item in row_range:
    employee_number = driver.find_element_by_xpath('//*[@id="employeeListGrid"]/div/div/div[6]/div/div/div[1]/div/table/tbody/tr[' + str(item) + ']/td[3]').text
    os.mkdir('export/' + str(employee_number))
    driver.find_element_by_xpath('//*[@id="employeeListGrid"]/div/div/div[6]/div/div/div[1]/div/table/tbody/tr[' + str(item) + ']/td[3]').click()
    time.sleep(2)
    ''' Retrieve the dictionary of all current employee files '''
    file_list = s.get('https://accudata.myisolved.com/api/EmployeeManagementDocumentApi')
    file_list_json = file_list.json()
    file_id_list = [] #create a list of file ids

    for x in file_list_json['pageData'][0].keys(): #the file list has separate dictionary for each category
        for y in file_list_json['pageData'][0][x]: #iterate through each document in each category
            file_id_list.append(y)  
    image_extension = (".JPG", ".JPEG", ".PNG", ".BMP", ".HEIC")


    for x in file_id_list:
        if str(x["fileName"]).upper().endswith(image_extension):
            '''Image files need to be downloaded using control + s '''
            s.post('https://accudata.myisolved.com/ViewReport.aspx', data={'AttachmentId': x["id"]})
            driver.execute_script('''window.open("https://accudata.myisolved.com/ViewReport.aspx", "_blank");''')
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)
            pyautogui.hotkey('ctrl', 's')
            time.sleep(5)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.typewrite('export/' + x["fileName"])
            pyautogui.hotkey('enter')
            time.sleep(15)
            dirpath = 'export'
            downloaded_file = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
            os.rename("export/" + str(downloaded_file[0]), "export/" + str(employee_number) + "/" + str(x["id"]) + "_" + str(x["fileName"]))
            driver.close()
            driver.switch_to.window(driver.window_handles[0])        
        else:
            '''PDF's and other documents will be downloaded automatically'''
            s.post('https://accudata.myisolved.com/ViewReport.aspx', data={'AttachmentId': x["id"]})
            driver.execute_script('''window.open("https://accudata.myisolved.com/ViewReport.aspx", "_blank");''')
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(15)
            dirpath = 'export'
            downloaded_file = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
            os.rename("export/" + str(downloaded_file[0]), "export/" + str(employee_number) + "/" + str(x["id"]) + "_" + str(x["fileName"]))
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_xpath('/html/body/form/div[4]/div[2]/span[2]/div/div[2]/div[1]/div[1]/a[1]/i').click() #return to employee list
    time.sleep(2)


