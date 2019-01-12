from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import os
import requests
import shutil
from xlsxwriter import Workbook

# advice: use delays to avoid getting blocked, try torrequest for changing your IP
# driver.switch_to.window(driver.window_handles[1]) changig active tab in driver chrome
chromePath="D:\\neco skola i rabota\\rabota\\learning dollars\\ChromeDriver\\chromedriver"

class App:
    def __init__(self,username='leposava10.02',password='WebScraper',targetUser='lence1970',path="D:\\neco skola i rabota\\rabota\\learning dollars\\instaScrape"):
        self.username=username
        self.password=password
        self.targetUser=targetUser
        self.path=path
        self.driver=webdriver.Chrome("D:\\neco skola i rabota\\rabota\\learning dollars\\ChromeDriver\\chromedriver")
        self.driver.get("https://instagram.com")
        self.error=False

        self.logIn()
        if self.error is False:
            self.openTargetProfile()
        if self.error is False:
            self.scrollDown()

        if not os.path.exists(path) and self.error is False:
            os.mkdir(path)

        if self.error is False:
            self.downloadImages()


        if self.error is False:
            self.getCaptions()

        print("Scraper has finished scraping!!!")
        self.driver.close()

    def getCaptions(self):
        try:
            file=Workbook(self.path+"\\captions.xlsx")
            worksheet=file.add_worksheet()


            sleep(2)
            soup=BeautifulSoup(self.driver.page_source,'lxml')
            allImgs=soup.find_all('div',attrs={'class':['v1Nh3','kIKUG',' _bz0w']})
            for index,img in enumerate(allImgs):
                link="https://instagram.com"+img.a['href']
                self.driver.get(link)
                sleep(2) #wait for content to load
                soup=BeautifulSoup(self.driver.page_source,'lxml')
                try:
                    caption=soup.find('div',attrs={'class':'C4VMK'}).span.string
                except Exception:
                    caption="No caption available"

                i=index+1 #because profile photo downloaded has index 0
                imgTxt='image'+str(i)+'.jpg'
                worksheet.write(index,0,imgTxt)
                worksheet.write(index,1,caption)


        except Exception:
            print("getCaptions Exception")
            self.error=True
        finally:
            file.close() # you must close the file

    def downloadImages(self):
        try:
            sleep(2)
            soup=BeautifulSoup(self.driver.page_source,'lxml')
            allImgs=soup.find_all('img')
            print(len(allImgs))

            for index,img in enumerate(allImgs):
                fileName="image"+str(index)+".jpg"
                imagePath=os.path.join(self.path,fileName)
                link = img['src']
                response=requests.get(link,stream=True)
                print("downloading image:"+str(index))
                try:
                    with open(imagePath,'wb') as file:
                        shutil.copyfileobj(response.raw,file)
                except Exception:
                    self.error=True
                    print("Error writing to disk")

        except Exception:
            self.error=True
            print("error while downloading")

    def scrollDown(self):
        try:
            sleep(2)
            nPosts=self.driver.find_element_by_class_name("g47SY")
            nPosts=str(nPosts.text).replace(',',"") #for bigger numbers
            nPosts=int(nPosts)
            self.nPosts=nPosts
            if(self.nPosts>12):
                nScrolls=int(self.nPosts/12)+3
                for val in range(nScrolls):
                    #print(val)
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    sleep(1)
        except Exception:
            self.error=True
            print("Problem with scroll down")



    def openTargetProfile(self):
        try:
            sleep(1) #it's better to wait 1s than having a bug
            searchBar=self.driver.find_element_by_xpath("//input[@placeholder='Search']")
            searchBar.send_keys(self.targetUser)
            sleep(1) #wait for results to show up
            targetUrl="https://instagram.com/"+self.targetUser+"/"
            self.driver.get(targetUrl)
            sleep(3)
        except Exception:
            self.error=True
            print("Openning profile error")

    def logIn(self):
        try:
            sleep(1)
            loginBtn=self.driver.find_element_by_link_text("Log in")
            loginBtn.click()

            sleep(3) #must sleep, because it needs some time to load the page !!!

            userNameTxt=self.driver.find_element_by_xpath("//input[@name='username']")
            passTxt=self.driver.find_element_by_xpath("//input[@name='password']")
            userNameTxt.send_keys(self.username)
            passTxt.send_keys(self.password)
            passTxt.submit()
            sleep(2) #wait page to load
            notNowBtn=self.driver.find_element_by_xpath("//button[@class='aOOlW   HoLwm ']") # do not turn on notifications
            notNowBtn.click()
        except Exception:
            self.error=True
            print("Log in error")



if __name__=='__main__':
    app=App()


