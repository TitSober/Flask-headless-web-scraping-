import time

from selenium import webdriver
from plyer import notification
from bs4 import BeautifulSoup
import smtplib


def sendMail(receipient,site):
    content = ("Posodobitev strani %s \n" % site)


    mail=smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    sender='avtonetscraper@gmail.com'
    
    mail.login('avtonetscraper@gmail.com','hhaalloo123')

    header='To:'+receipient+'\n'+'From:'\
    +sender+'\n'+'subject:Novo obvestilo\n'
    content = header+content
    mail.sendmail(sender,receipient, content)
    mail.close()

def web_scrape(u,e):
  browser = webdriver.Firefox()
  browser.set_window_size(1280, 720)
  url = u #tukaj bomo menjali url za stran katero hočemo nadzarovati
  
  

  browser.get(url)
  browser.implicitly_wait(10)
  soup = BeautifulSoup(browser.page_source, "html.parser")
  form = soup.find_all(class_='GO-Results-Row')
  def removeImages(soup):
    for data in soup(['style', 'script','img']):
          # Remove tags
          data.decompose()
    
      # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

  if "https://ct.captcha-delivery.com/c.js" in soup:
      
      notification.notify(
        title = 'Ran into CATCHA',
        message = 'Solve captcha first and then proceed',
        app_icon = None,
        timeout = 10,)
      time.sleep(30)    
  form = removeImages(form[len(form)-1])
  #with open('test.txt','w') as f:
  #      f.write(str(form[0]))
  #      f.write("\n\n\n\n\n----------------------------------------------------------------------------\n\n\n")


  proceed = True

  while(proceed):
    if "https://ct.captcha-delivery.com/c.js" in soup:
      proceed = False
      notification.notify(
        title = 'Ran into CATCHA',
        message = 'Solve captcha first and then proceed',
        app_icon = None,
        timeout = 10,)
      time.sleep(30)

    print("loops")
    browser.get(url)
    browser.implicitly_wait(5)
    new_form = BeautifulSoup(browser.page_source,"html.parser").find_all(class_='GO-Results-Row')
    new_form = removeImages(new_form[len(new_form)-1])
    if(form != new_form):#preveri ali se je stran spremenila

      #debug feature
      notification.notify(
      title = 'Something updated',
      message = url+ ' updated',
      app_icon = None,
      timeout = 10,)


      sendMail(e,str(u))
      #with open('test.txt','a') as f:
      #  f.write(str(new_form[0]))

      proceed = False

      



      form = new_form #prepiše nov html v spremenljivko   

    else:
      pass
    time.sleep(6)#počaka 1 minuto in nato nadaljuje loop

  browser.quit()

#web_scrape("https://www.avto.net/Ads/results.asp?znamka=Peugeot&model=&modelID=&tip=katerikoli%20tip&znamka2=&model2=&tip2=katerikoli%20tip&znamka3=&model3=&tip3=katerikoli%20tip&cenaMin=0&cenaMax=999999&letnikMin=0&letnikMax=2090&bencin=0&starost2=999&oblika=0&ccmMin=0&ccmMax=99999&mocMin=&mocMax=&kmMin=0&kmMax=9999999&kwMin=0&kwMax=999&motortakt=&motorvalji=&lokacija=0&sirina=&dolzina=&dolzinaMIN=&dolzinaMAX=&nosilnostMIN=&nosilnostMAX=&lezisc=&presek=&premer=&col=&vijakov=&EToznaka=&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000000000&EQ7=1000000120&EQ8=1010000001&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&PSLO=&akcija=&paketgarancije=&broker=&prikazkategorije=&kategorija=&ONLvid=&ONLnak=&zaloga=&arhiv=&presort=&tipsort=&stran=","tit")