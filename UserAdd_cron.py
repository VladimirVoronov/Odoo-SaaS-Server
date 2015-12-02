# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################


from UserAdd import myodoo_register
import os
import sys
from lxml import etree

sys.path.append('/home/vovan/eclipse/demo_robot')
sys.path.append('/opt/openerp/register_robot')

#cd  /home/vovan/eclipse/demo_robot
#python UserAdd_cron.py
#python /home/vovan/eclipse/demo_robot/UserAdd_cron.py
class cron_robot():
	def __init__(self):
		print 'Init cron robot'
		self.local_path=os.getcwd()
		#self.local_path='/opt/openerp/register_robot'
		
		for curr in os.listdir(self.local_path+'/procc'):
			if curr[-4:]!='.xml':continue
			file_path=self.local_path+'/procc/'+ curr
			self._parse_xml(file_path)
			
			
		print 'End cron robot'
		
	def _parse_xml(self, file_path):
		print file_path
		md=myodoo_register()

		tree = etree.parse(file_path)
		root=tree.getroot()
		
		for curr in root:
			#print curr.tag
			#print curr.text
			#print type(curr.text)
			setattr(md, curr.tag, unicode(curr.text))
			
		md.add_user()
		
		md.print_sip_info()
		md.print_odoo_info()
		os.rename(file_path, self.local_path+'/storage/'+ md.account+'.xml')

if __name__ == "__main__":		
	cr=cron_robot()