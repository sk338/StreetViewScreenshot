from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import time
import os
import csv

base_url = 'https://google.com/maps/search/'

chrome_options = Options()
# chrome_options.add_argument('start-maximized')
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=3840,2160")    # 1920x1080 * 2dpi = 3840x2160
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=
                          Service(ChromeDriverManager().install()), options=chrome_options)
# driver.maximize_window()


def streetViewScreenshot(mergedAddress, address):
    driver.get(base_url)
    driver.implicitly_wait(5)
    driver.find_element(By.ID, 'searchboxinput').send_keys(mergedAddress)
    driver.find_element(By.ID, 'searchbox-searchbutton').click()
    time.sleep(5)

    # screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.
    # X, Y = pyautogui.position() # Get the XY position of the mouse.
    # print(screenWidth, screenHeight)
    # print(X, Y)
    # driver.find_element(By.CSS_SELECTOR, '#QA0Szd button.aoRNLd').click()

    mapYear = ''
    for span in driver.find_elements(By.TAG_NAME, 'span'):
        if 'Map data ©' in span.text:
            # print(f"Map data year: {span.text.replace('Map data ©','').strip()}")
            mapYear = span.text.replace('Map data ©','').strip()
            break

    # pyautogui.click(165, 245)
    try:
        driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div['
                                      '1]/button/img').click()
    except:
        pass

    time.sleep(6)

    imageType = 'Picture'
    for span in driver.find_elements(By.TAG_NAME, 'span'):
        if 'Map data ©' in span.text:
            # print("Map data")
            imageType = 'Map data'
            break

    imageCaptureDate = ''
    for span in driver.find_elements(By.TAG_NAME, 'span'):
        if 'Image capture:' in span.text:
            # print(f"Image capture date: {span.text.replace('Image capture: ','').strip()}")
            imageCaptureDate = span.text.replace('Image capture: ','').strip()
            break

    driver.save_screenshot(os.getcwd() + "\\images\\" + mergedAddress + ".jpg")

    try:
        final_data = [mergedAddress + '.jpg', *address, str(mapYear),
                      str(imageCaptureDate), imageType, str(driver.current_url)]

        finalstr = ''
        for j in final_data:
            if ',' in j:
                finalstr = f'{finalstr}"{j}",'
            else:
                finalstr = f'{finalstr}{j},'

        finalstr = finalstr[:-1]
        # print(finalstr)
        Output_Handle.write(f'{finalstr}\n')
        Output_Handle.flush()

    except Exception as e:
        print(str(e))
        Output_Handle.close()


with open('AddressSheet.csv', newline='') as f:
    reader = csv.reader(f)
    addresses = list(reader)

# save the image name, address, image date

outputFileName = 'AddressOutput.csv'

if os.path.isfile(outputFileName):
    Output_Handle = open(outputFileName, 'a')
else:
    Output_Handle = open(outputFileName, 'a')
    Output_Handle.write('filename,address,city,state,zipcode,map_year,image_captured_date,image_type,link\n')

for i, address in enumerate(addresses):
    if i > 0:
        mergedAddress = ' '.join(address)
        print(f'Working on image {i} of {len(addresses)}. Saved -> {mergedAddress}.jpg')
        streetViewScreenshot(mergedAddress, address)

driver.quit()
Output_Handle.close()