#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests,time,smtplib
from bs4 import  BeautifulSoup
from notify_run import Notify
from datetime import datetime


# In[2]:


url = "https://www.amazon.in/Apple-MacBook-13-inch-1-4GHz-Quad-core/dp/B07V2GVWKK/ref=sr_1_3?keywords=macbook+pro&qid=1569665731&refinements=p_n_feature_browse-bin%3A1485945031%7C1485947031&rnid=1464448031&s=computers&sr=1-3"
dp = 120000
URL = url
#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}


# In[3]:


page = requests.get(URL)
 
soup= BeautifulSoup(page.content,'html.parser')


# In[4]:


m=open('soupw.txt',"wb")
m.write(soup.prettify().encode("utf-8"))
m.close


# In[5]:


title = soup.find(id="productTitle").get_text()
price = soup.find(id="priceblock_ourprice").get_text()
main_price = price[2:]
#print(title,price)


# In[6]:


import re
main_price=main_price.split('.')[0]
main_price1 = re.sub('[^0-9]+','',main_price)
print(main_price1)


# In[7]:


title1=title.strip()


# In[8]:


def check_price():
    count = 0
    if(int(main_price1) <= dp):
        send_mail()
        push_notification()
    else:
        count = count+1
        print("Rechecking... Last checked at "+str(datetime.now()))


# In[9]:



def send_mail():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
 
    server.login(email_id,password)
 
    subject = "Price of "+title1+" has fallen down to Rs. "+str(main_price1)
    body = "Hey Anurag! \n The price of "+title1+" on AMAZON has fallen down to Rs."+str(main_price1)+", which is less than your desired price of Rs."+str(dp)+".\n So, hurry up & check the amazon link right now : "+url
 
    msg = f"Subject: {subject} \n\n {body} "
 
    server.sendmail(
        email_id,email_id,
        msg
    )
    print("HEY Anurag, EMAIL HAS BEEN SENT SUCCESSFULLY.")
 
 
    server.quit()


# In[10]:


pnmsg="Rs. "+str(main_price1)+" for "+title1
def push_notification():
    notify = Notify()
    notify.send(pnmsg)
    print("HEY Anurag, PUSH NOTIFICATION HAS BEEN SENT SUCCESSFULLY.")
    
    print("Check again after an hour.")


# In[11]:


count = 0
while(True):
    count += 1
    print("Count : "+str(count))
    check_price()
    time.sleep(60)

