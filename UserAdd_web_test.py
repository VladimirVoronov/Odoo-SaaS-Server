# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################
import sys
from splinter import Browser
sys.path.append('/home/vovan/eclipse/PaseBook')
from invents import invents
import urllib2
import time
import os

import socks
import socket
import httplib2

proxy_settings = {'network.proxy.type': 1,
       'network.proxy.socks': 'localhost',
       'network.proxy.socks_port': 8080,
       'network.proxy.socks_version': 4,  
       'network.proxy.no_proxies_on':'',   
      }

browser = Browser('firefox', profile_preferences=proxy_settings)
# Visit URL

url = "http://www.myodoo.ru:9080/"

browser.visit(url+'register/')

inn=invents()
inn.generate()
inn.generate_firstname()

email=inn.generate_email()
email=email.replace('.','')
email='zz'+email
email=email.lower()

wp=inn.generate_work_place(1982)
user_company=wp['company']
user_company=user_company.replace('"','')
user_company=user_company.replace('-','')
user_company=user_company.replace('.','')
user_company=user_company.replace(',','')
		
browser.find_by_name('db_name').last.fill(email)
browser.find_by_name('login').last.fill(email+'@arterp.ru')
browser.find_by_name('name').last.fill(inn.FirstName+' '+inn.LastName)
browser.find_by_name('phone').last.fill(inn.generate_phone2())
browser.find_by_name('company').last.fill(user_company)
browser.find_by_id('submit_button').first.click()

sms_url=url+'get_code/%s' % email

httplib2.debuglevel=0
h = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_SOCKS4, 'localhost', 8080))
r,c = h.request(sms_url)

print c

browser.find_by_name('phone_code').last.fill(c)
browser.find_by_name('button').first.click()

browser.quit()
print 'done'

#os.WEXITSTATUS(os.system('sudo /etc/add_host.sh %s.myodoo.ru' % email))


c="/opt/myodoo/register_robot/UserAdd.sh"
command='ssh root@10.0.0.100 "'+ c+'"'

#print command
#os.WEXITSTATUS(os.system(command))


#from UserAdd_cron import cron_robot
#cr=cron_robot()

#time.sleep(20)

#from UserDelete import UserDel
#ud=UserDel(email)
#ud=UserDel('pugassigorogo')
