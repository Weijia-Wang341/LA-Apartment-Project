from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import csv

MAX_PAGE_NUM = 2
MAX_PAGE_DIG = 1
s=Service("C:\Program Files (x86)\chromedriver.exe")
driver=webdriver.Chrome(service=s)
driver.maximize_window()
mylat = []
mylng = []


with open('apt_results.csv', 'w') as f:
    f.write("Name,Price,Bed,Info,Address,Link,Lat,Lng\n")


for i in range(1, MAX_PAGE_NUM + 1):
    page_num = (MAX_PAGE_DIG - len(str(i))) * "0" + str(i)
    url = "https://www.apartments.com/los-angeles-ca/" + page_num
    #print(url)

    driver.get(url)
    driver.implicitly_wait(10)

    aprice=driver.find_elements(By.XPATH,"//p[contains(@class,'property-pricing')]")

    alink=driver.find_elements(By.XPATH,"//a[contains(@class,'property-link js')]")

    ainfo=driver.find_elements(By.XPATH,"//p[contains(@class,'property-amenities')]")

    aaddress=driver.find_elements(By.XPATH,"//div[contains(@class,'property-address')]")

    aname=driver.find_elements(By.XPATH,"//span[contains(@class,'js-pla')]")

    abed=driver.find_elements(By.XPATH,"//p[contains(@class,'property-beds')]")

    myprice=[]
    mybed=[]
    myinfo=[]
    myaddress=[]
    myname=[]
    mylink=[]

    for price in aprice:
        #print(price.text)
        myprice.append(price.text)
    for link in alink:
        #print(link.get_attribute("href"))
        mylink.append(link.get_attribute('href'))
    for info in ainfo:
        #print(info.text)
        myinfo.append(info.text)
    for address in aaddress:
        #print(address.text)
        myaddress.append(address.text)
    for name in aname:
        #print(name.text)
        myname.append(name.text)
    for bed in abed:
        mybed.append(bed.text)


    finallist=zip(myname,myprice,mybed,myinfo,myaddress,mylink)
    #for data in list(finallist):
    #   print(data)
    with open('apt_results.csv', 'a', newline='') as f:
        thewriter = csv.writer(f)
        #thewriter.writerow(['name', 'price', 'bed', 'info','address','link'])
        for row in list(zip(myname,myprice,mybed,myinfo,myaddress,mylink)):
            thewriter.writerow(row)





driver.quit()
