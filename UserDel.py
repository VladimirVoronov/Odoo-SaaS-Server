# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################
import os
import re
import shutil
import polib
import ConfigParser
import logging
import os
import sys
from lxml import etree

from ConfigParser import SafeConfigParser

from UserAdd import myodoo_register

class UserDel(myodoo_register):
	def __init__(self, account):
		self.account=account
		self.read_config()
		self.command_prefix=''
		
		logging.basicConfig(filename=self.log_file, level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
		logging.info('Init User Add')
		self._parse_xml()
		
	def _parse_xml(self):
		self.local_path=os.getcwd()
		#self.local_path='/opt/openerp/register_robot'
		
		self.xml_path=self.local_path+'/storage/'+ self.account+'.xml'
		print self.xml_path

		tree = etree.parse(self.xml_path)
		root=tree.getroot()
		
		for curr in root:
			setattr(self, curr.tag, unicode(curr.text))
			
		self.start_del()	
		#os.remove(self.xml_path)
		
	def start_del(self):

		drop_sh="""#!sh
		psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{ account }';" -d { account }
		dropdb -w { account }
		
 		gpasswd -d root  { account }
		gpasswd -d myodoo { account }
		gpasswd -d asterisk { account }
		
		userdel { account }
		rm -r /home/{ account }
		"""
		self.exe(drop_sh)
		self.init_vals()
		
		#Post section
		self.exe('-'+self.add_alias1)
		self.exe('-'+self.add_alias2)
		self.exe(self.add_resresh_post)
		
		#SIP section
		self.exe('-'+self.add_sip)
		self.exe('-'+self.add_extension1)
		self.exe('-'+self.add_extension2)
		self.exe(self.add_resresh_sip)
		
		self.add_confirm="""#!sh
		wget http://www.myodoo.ru:9080/base_del/{ account } > /tmp/{ account }.html
		"""
		
		self.exe('-'+self.hosts)
		self.exe(self.add_confirm)
		

