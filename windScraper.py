from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests
import pytz
from datetime import datetime
import csv
def saveToCSV(results):
    save_file = input("Save File Name : ")
    save_file = save_file if('.csv' in save_file) else save_file + '.csv'
    csv_columns = ['TIME','DIRECTION','STRENGTH(km/h)','DESCRIPTION']
    with open(save_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in results:
            writer.writerow(data)

def main():
    if(__name__ == '__main__'):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)
        #driver = uc.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options,use_subprocess = True)

        #driver.delete_all_cookies()
        print("----Starting Program---")
        location = input("Location : ")
        #website_file = 'sites.txt'
        print("Getting to website")
        driver.get('https://wind.willyweather.com.au/')
        print("Moving to wind panel")
        driver.find_element(By.XPATH,'/html/body/section/section[2]/main/nav/section[1]/a[2]').click()
        sleep(5)
        print("Running Search")
        driver.find_element(By.XPATH,'/html/body/section/section[1]/form/input').send_keys(location)
        sleep(2)
        a_tag = driver.find_element(By.XPATH,'/html/body/section/section[1]/form/div/ul/li[2]/a')
        href = a_tag.get_attribute('href')
        driver.get(href)
        #driver.find_element(By.XPATH,'/html/body/section/section[1]/form/input').send_keys(Keys.RETURN)
        sleep(5)
        print("Changing to 1 day")
        #driver.find_element(By.XPATH,'/html/body/section/section[2]/main/article/nav/a[1]').click()
        #sleep(5)
        dt = datetime.now()
        now = dt.astimezone(pytz.timezone('Australia/Sydney'))
        graph_href = driver.find_element('xpath','/html/body/section/section[2]/main/article/form/fieldset/legend/a').get_attribute('href')
        json_href = graph_href.replace('graphs.html?','graphs/data.json?startDate=' + str(now.date()) + '&')
        print(json_href)
        r  = requests.get(json_href, headers={'X-Requested-With': 'XMLHttpRequest'})
        data = r.json()
        wind_data = data['data']['forecastGraphs']['wind']['dataConfig']['series']['groups']
        results = []
        for data in wind_data:
            points = data['points']
            for point in points:
                timestamp = point['x']
                time = datetime.fromtimestamp(timestamp,pytz.timezone('Africa/Dakar'))
                if(time.date() == now.date()):
                    hour = time.hour
                    hour = (str(hour) + ':00 AM') if(hour <= 12) else (str(hour-12) + ':00 PM') 
                    if(time.hour == 0):
                        hour = '0:00 AM'
                    results.append({
                        'TIME': hour ,
                        'DIRECTION' : point['directionText'],
                        'STRENGTH(km/h)' : point['y'],
                        'DESCRIPTION' : point['description']
                        })
                if(time.date() > now.date()):
                    print(results)
                    saveToCSV(results)
                    quit()

main()