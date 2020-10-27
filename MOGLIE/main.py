import time
from decouple import config
import json
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from yattag import Doc
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



class movie_offer_getter():

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.bank_name = config('BANK_NAME')
        self.city_name = config('CITY')
        self.save_html = config('SAVE_HTML')
        self.offer_count = 0
        self.base_link = 'https:\\in.bookmyshow.com'
        self.image_url_dict={}
        self.receiver_email = config('RECEIVER_EMAIL_ID')
        self.sender_email = config('SENDER_EMAIL_ID')
        self.sender_pass = config('SENDER_PASSWORD')


    def build_offer_dict(self):
        """
        Uses webdriver to go bookmyshow.com
        Finds Offers on the page 
        Grabs the offer images and the urls for our email
        Compiles them into a dictionary(hashmap) of the format {Image_location : Offer_Url}
        """

        #Maximize the window and go to the website
        self.driver.maximize_window()
        self.driver.get(self.base_link)
        time.sleep(4)

        try:
            ok = self.driver.find_element_by_xpath('//*[@id="wzrk-confirm"]')
            ok.click()
        except:
            pass

        # The website has a hover-over mechanism to reveal cities within each sector
        city_to_select = self.driver.find_element_by_xpath("//*[@id='modal-root']/div/div/div/div[2]/ul/li[1]/div/div/img")
        hover = ActionChains(self.driver).move_to_element(city_to_select)
        hover.perform()

        # Select our city
        print('Searching for our desired city')
        city = self.driver.find_element_by_xpath("//*[contains(text(),'"+self.city_name+"')]")
        city.click()
        time.sleep(1)
        print('City selected')

        # Go the Offers Page
        print('Looking for offers page')
        offers_link = self.driver.find_element_by_partial_link_text('Offers')
        offers_link.click()
        print('Found Offers page')

        # Get all the offers on the page
        offers =self.driver.find_elements_by_xpath("//*[@class= 'card offer-card _loaded']")

        print("Filtering offers by user's bank account")
        self.image_url_dict ={}
        for offer in offers:
            offer_url = offer.get_attribute('data-url')
            if self.bank_name in offer_url:
                sc_name = 'images/'+str(self.offer_count)+'.png'
                offer.screenshot(sc_name)
                self.offer_count+=1
                self.image_url_dict[offer_url] = sc_name
        
        print('Total Offers Found:',self.offer_count)

    def convert_to_html(self):
        """
        Take the offers dictionary prepared and convert it into a clean HTML with clickable images
        The output of this stage shall be sent to the auto emailer 
        """
        count = 0
        doc, tag, text = Doc().tagtext()
        offers  = self.image_url_dict
        with tag('html'):
            with tag('div',style= 'text-align: center'):
                doc.stag('img', src='cid:banner')
            with tag('body'):
                for offer in offers:
                    with tag('div',style= 'text-align: center'):
                        with tag('a', href=self.base_link+offer):
                            doc.stag('img', src='cid:img'+str(count))
                            count+=1


        self.html_content = doc.getvalue()
        if self.save_html:
            f = open('output.html','w+')
            f.write(self.html_content)
            f.close()

    def send_offer_email(self):
        '''
        Send an email to the recipient using the html content created
        '''

        msg =  MIMEMultipart('related')#EmailMessage()
        msg['Subject']= 'Customized Movie Offers'
        msg['From'] = 'Movie Offers <kredozoid@gmail.com>' 
        msg['To'] = self.receiver_email
        mail_server = 'smtp.gmail.com'

        #msg.add_alternative(self.html_content,subtype='html')
        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)

        # We reference the image in the IMG SRC attribute by the ID we give it below
        msgText = MIMEText(self.html_content, 'html')
        msgAlternative.attach(msgText)

        print('Preparing Email')
        # Do it once for banner
        fp = open('images/banner.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        msgImage.add_header('Content-ID','<banner>')
        msg.attach(msgImage)

        count = 0
        for offers in self.image_url_dict:
            fp = open(self.image_url_dict[offers], 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
        
            msgImage.add_header('Content-ID','<img'+str(count)+'>')
            count+=1
            msg.attach(msgImage)
        print('Email Ready')

        print('Sending Email...')
        smtp = smtplib.SMTP_SSL(mail_server,465)
        smtp.login(self.sender_email,self.sender_pass)
        smtp.send_message(msg)
        smtp.quit()
        print('Email Sent')

        #except Exception:
        #    print('unable to send email')


if __name__ == "__main__":
    mog = movie_offer_getter()
    mog.build_offer_dict()
    mog.convert_to_html()
    mog.send_offer_email()
