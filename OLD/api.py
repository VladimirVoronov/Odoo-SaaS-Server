# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################
import os

import xmlrpclib


class base_api():
	def __init__(self):
		self.command_prefix=''
		self.log=[]
		
		self.user='root'
		self.host='192.168.1.110'
		self.script_storage='/home/vovan/Linux/scripts/'
		
		self.fs_storage_path='/opt/odoo-master/'
		
		self.command_prefix='ssh '+self.user+'@'+ self.host
		
		if not self.host:
			self.command_prefix=''
			
	def exe_local(self, command):
		res=os.WEXITSTATUS(os.system(command))
		if self.debug_mode:
			print 'Result execute command %s' % str(res)
		return res
	def exe_command(self, command):
		if type(command) is list:
			for comma in  command:
				self.exe_command(comma)
		
		if type(command) is str:
			command=self.command_prefix+' "'+ command+'"'
			#print 'Try execute command= %s' % command
			res=os.WEXITSTATUS(os.system(command))
			
			#print 'Result execute command %s' % str(res)
			return res
	def add_file(self, file):
		comm=''
		#self.exe_command('apt-get update')
		
	def update_system(self):
		self.exe_command('apt-get update')
		self.exe_command('apt-get upgrade')
			
	def del_row_from_file(self, row, file):	
		#sed -i '/^Ваша строка$/d' "путь к файлу в котором надо удалить"
		#очевидно же, что слеш - это спец. символ... их надо экранировать. ну и по поводу кавычек уже написал фикс...
		#sed -i '/^linux addons\/dproto\/dproto_i386.so$/d' "home/cgss/service16/cs/cstrike/addons/metamod/plugins.ini"
		pass
	
	def copy_file(self, file_name, dest):
		local_path=self.script_storage+file_name
		cmd='scp %s %s@%s:%s' % (local_path, self.user, self.host, dest) 
		print cmd
		self.exe_command(cmd)
		
	def add_row_to_file(self, file, txt):
		comm="sed -i '$ a %s' %s" % (txt, file)

		self.exe_command(comm)

	def add_row_to_file_after(self, file, txt, after):
		comm="sed -i '/%s/a %s' %s" % (after, txt, file)
		print comm
		self.exe_command(comm)
			
	def add_log(self, mess):
		print mess
		self.log.append(mess)
		
	def exe_sql(self, sql):
		comm='psql -c \\"%s;\\" -d %s' % (sql, self.account)
		self.exe_command(comm)
		
	def change_access_mode(self):
		comm=[
		'chown -R root:openerp %s' % self.fs_storage_path,
		'chmod -R 770 %s' % self.fs_storage_path,
		'chmod +x %sopenerp-server' % self.fs_storage_path,
		
		]
		
		self.exe_command(comm)