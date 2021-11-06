from ip2geotools.databases.noncommercial import DbIpCity
import requests
from selenium import webdriver
r = requests.get("https://get.geojs.io/")
ip_request=requests.get("https://get.geojs.io/v1/ip.json")
ipAdd=ip_request.json()['ip']

url="https://get.geojs.io/v1/ip/geo/"+ipAdd+'.json'
geo_request=requests.get(url)
geo_data=geo_request.json()
timezone=geo_request.json()['timezone']
country=geo_request.json()['country']

#print(country)
city=DbIpCity.get(ipAdd,api_key="free")

#print(country)
location=city.region+","+country
def showingposition():
 current_location="You are currently in "+timezone+"  ,exactly in,  "+location
 print(current_location)
 driver = webdriver.Chrome("C://Users/khaoula/Desktop/5arya/chromedriver")
 driver.get("https://www.google.com/maps")
        #driver.set_window_position()
 driver.set_window_size(10, 700)
 driver.set_window_position(180,18)




 loc=driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/form/div/div[3]/div/input[1]")
 loc.send_keys(location)

 submit = driver.find_element_by_xpath( "/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button")
 submit.click()

