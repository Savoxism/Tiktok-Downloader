import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.request import urlopen

'''
Links For This Project:
https://curlconverter.com/
https://ssstik.io/en
'''

def downloadVideo(link, id):
    print(f"Downloading video {id} from: {link}")
    cookies = {
    'cf_clearance': 'stsmOZ9SxrLY6ZyQr4Lj53FhPUdQkcYDH45gtShCkTU-1708757420-1.0-ATj9s9BB7ktR2KKP+PDoTOgwVgnO3206NNoZkRRFQ3rSoCalAFPtxWkaE7+620Ac45xcnlqbLWdYLk9eqRpccsg=',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'cf_clearance=stsmOZ9SxrLY6ZyQr4Lj53FhPUdQkcYDH45gtShCkTU-1708757420-1.0-ATj9s9BB7ktR2KKP+PDoTOgwVgnO3206NNoZkRRFQ3rSoCalAFPtxWkaE7+620Ac45xcnlqbLWdYLk9eqRpccsg=',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-arch': '"arm"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"121.0.6167.184"',
        'sec-ch-ua-full-version-list': '"Not A(Brand";v="99.0.0.0", "Google Chrome";v="121.0.6167.184", "Chromium";v="121.0.6167.184"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"14.2.1"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'NDN5NTY4',
    }

    print("Step 4: Obtaining the download link")
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")
    downloadLink = downloadSoup.a["href"]
    
    print("Step 5: Saving the video :)")
    mp4File = urlopen(downloadLink)
    with open(f"/Users/nguyenphuan/Documents/programming/tiktok/{id}.mp4", "wb") as output: #This needs to be a file 
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break
            
#Initialize the Chrome browser
print("Step 1: Opening Chrome")
options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=options)
driver.get("https://www.tiktok.com/@swissaround") #Insert desired TikTok channel here
time.sleep(15)

#Continue as guest
continue_as_guest = driver.find_element(by = By.XPATH, value = '//*[@id="loginContainer"]/div/div/div[3]/div/div[2]')
continue_as_guest.click()
time.sleep(10)

#Scroll down the page
scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

print("Step 2: Scroll till the end of the page")
while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break 
    
#Interact with the videos
className = " css-1as5cen-DivWrapper e1cg0wnj1" #Inspect elements to find this variable

script  = "let l = [];"
script += "document.getElementsByClassName(\""
script += className
script += "\").forEach(item => { l.push(item.querySelector('a').href)});"
script += "return l;"

urlsToDownload = driver.execute_script(script)

print(f"Step 3: There are {len(urlsToDownload)} videos in total")
for index, url in enumerate(urlsToDownload):
    print(f"Downloading video: {index}")
    downloadVideo(url, index)
    time.sleep(10)
    
