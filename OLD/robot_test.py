# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################

import sys
sys.path.append('/home/vovan/eclipse/PaseBook')
from robot import robot
import random

#ssh -f -N -L 3832:127.0.0.1:5432 root@192.168.1.110
#sshfs root@192.168.1.110:/ /mnt/Notebook
# chmod 777 /opt/openerp

#/etc/init.d/openerp-server restart
#/etc/init.d/asterisk restart
#andreyakushe.my.arterp.sru

#http://www.rjsystems.nl/en/2100-asterisk.php
#http://asterisk.ru/knowledgebase/Asterisk+config+extensions.conf

#Res name sip:1000@my.arterp.sru
## Comtube
#pliklo
# pEb2nauyWo2CfHQ2fUZp0DJQ2juUCHPr


#sip:539578@sip.comtube.com Настроить 
#sip:775983@sip.comtube.com

#http://andreyakushe.my.arterp.sru/phones/income?db=andreyakushe&phone=79054811212&user_id=38005
#http://www.uiscom.ru/services/virtual_ats.php

from invents import invents
inn=invents()
inn.generate()	

account=inn.generate_email()	
rb=robot(account)

vals={}

vals['user_name']=inn.FirstName+ ' '+ inn.LastName
work=inn.generate_work_place(1982)
vals['company_name']=work['company']

vals['user_email']=account+'@mail.sru'

phone=inn.generate_phone()
phone=phone.replace('','+7 ')
vals['user_phone']=phone

rb.add_account(vals)
#
abonent_phone=random.randint(20000, 60000)
abonent_pass=inn.generate_pass(len=12)

rb.add_asterisk(abonent_phone, abonent_pass)