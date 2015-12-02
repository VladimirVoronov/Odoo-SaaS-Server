# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################


from UserDel import UserDel
import os
import sys
from lxml import etree

class cron_robot():
	def __init__(self):
		print 'Init cron robot'
		self.local_path=os.getcwd()
		#self.local_path='/opt/openerp/register_robot'
		
		for curr in os.listdir(self.local_path+'/to_del'):
			if curr[-4:]!='.xml':continue
			file_path=self.local_path+'/to_del/'+ curr
			
			acc=curr.split('.')[0]
			ud=UserDel(acc)
			os.remove(file_path)
			
		print 'End cron robot'
		

if __name__ == "__main__":		
	cr=cron_robot()