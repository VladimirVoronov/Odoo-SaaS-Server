# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################
import sys
import random
import uuid

from lxml import etree

sys.path.append('/home/vovan/eclipse/PaseBook')
from invents import invents

class test_User_unit():
	
	def _generate_pass(self, len=8):
		def_chars = "234679ADEFGHJKLMNPRTUWabdefghijkmnpqrstuwy"
		
		ret_vals=''
		i=len
		
		while i >0:
			ret_vals+=random.choice(def_chars)
			i-=1
			
		return ret_vals	
	
	def __init__(self):
		pass
		#self.local_path=os.getcwd()
		#self.local_path='/opt/openerp/register_robot'
		
	def invent_user(self):
		inn=invents()
		inn.generate()
		
		inn.generate_firstname()
		
		self.account=inn.generate_email()
		
		#self.user_pass=inn.generate_pass()
		self.user_pass='qqq'
		self.abonent_phone=random.randint(20000, 60000)
		self.abonent_pass=inn.generate_pass()
		self.uuid=str(uuid.uuid1())
		
		self.user_name=inn.FirstName
		self.user_last_name=inn.LastName
		self.user_email=self.account+'@yandex.ru'
		wp=inn.generate_work_place(1982)
		self.user_company=wp['company']
		self.user_phone=inn.generate_phone()
		
	def dump_to_xls(self):
		
		root_branch= etree.Element("root")
		for attr in self.__dict__:
			xml=etree.Element(attr)
			xml.text=unicode(self.__dict__[attr])
			root_branch.append(xml)
			
		#result = etree.tostring(root_branch, pretty_print=True,  encoding='unicode')
		#tree.write('output.xml', pretty_print=True, xml_declaration=True)
		tree = etree.ElementTree(root_branch)
		tree.write(self.local_path+'/procc/'+self.account+'.xml', pretty_print=True, xml_declaration=True, encoding="UTF-8")
		print self.account
		
uu=test_User_unit()
uu.invent_user()
print uu.account+'@arterp.ru'
#uu.dump_to_xls()

#md=myodoo_register()
#md.account='Puga4eff'+str(random.randint(20000, 60000))
#md.add_user()
#md.print_sip_info()
#md.print_odoo_info()

#inn=invents()
#inn.invent_user()
#print inn.generate_email()+'@arterp.ru'