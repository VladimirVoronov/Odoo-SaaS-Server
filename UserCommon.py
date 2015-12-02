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

from ConfigParser import SafeConfigParser

class UserCommon():
	def __setattr__(self, name, value):
		if name=='ssh_user' or name=='ssh_host':
			self.__dict__[name]=value
			if self.__dict__.has_key('ssh_user') and self.__dict__.has_key('ssh_host') and self.ssh_user and self.ssh_host:
				self.__dict__['command_prefix']='ssh '+self.ssh_user+'@'+ self.ssh_host
			else:
				self.__dict__['command_prefix']=''
					
		if name=='account':
			account=value
			account=re.sub(r'[^0-9a-zA-Z]', '', account)
			account=account.replace('-', '')
			account=account.replace('_', '')

			self.__dict__['account']=account.lower()
		
			self.record_dir=self._command_parser('/home/{ account }/phone_records/')
			self.backup_dir=self._command_parser('/home/{ account }/backup/')
		else:	
			self.__dict__[name]=value
				
	def read_config(self, name='robot.conf'):
		config_path=os.getcwd()+'/'+name

		parser = SafeConfigParser()
		parser.read(config_path)
		print config_path

		for name, value in parser.items('Default'):
			setattr(self, name, unicode(value))
			
	def _command_parser(self, comm):
		for val in self.__dict__:
			comm=unicode(comm)
			val=unicode(val)
			#print comm
			#print val
			comm=comm.replace(u'{ '+val+u' }', self.__dict__[val])
		return comm
	
	def _exe_ssh(self, c):
		c=c.strip()
		if not c:
			print ''
			return False
		
		if self.command_prefix:
			command=self.command_prefix+' "'+ c+'"'
		else:
			command=c
			
		log_command=command		
		command=command.encode("UTF-8")
		
		if self.print_log=='1':
			print command
		
		log_command=log_command.replace(self.abonent_pass, '*****')
		log_command=log_command.replace(self.user_pass, '*****')	
		logging.debug(log_command)	
		
		res=os.WEXITSTATUS(os.system(command))
		
		if self.print_log=='1':
			print res

	def exe(self, comm):
		orig_comm=self._command_parser(comm)
		
		comm=orig_comm.split('\n')
		flag=comm[0]
		comm=comm[1:]
		
		if flag=='#!sh':
			for c in comm:
				self._exe_ssh(c)

		if flag=='#!SQL':
			for c in comm:
				c=c.strip()
				if not c:
					print ''
					continue
				comm='psql -c "%s;" -d %s' % (c, self.account)
				self._exe_ssh(comm)
		
		if flag.find('!!!!!!!!!-#!/')>=0 :
			file_name=flag.replace('-#!', '')
			insert_string=None
			
			print 'DEL file_name %s' % file_name
			
			if file_name.find('#')>0:
				cool=file_name.split('#')
				file_name=cool[0]
				insert_string=cool[1]
				
			orig_comm=orig_comm.replace(flag+'\n', '')
			#orig_comm='\\'+orig_comm
			#orig_comm=orig_comm.replace('\n', '\\n')
			#orig_comm=orig_comm.replace('\t', '.*')
			#orig_comm=orig_comm.replace('/', '\/')
			#orig_comm=orig_comm.replace('{', '.*')
			#orig_comm=orig_comm.replace('}', '.*')
			#orig_comm=orig_comm.replace('(', '.*')
			#orig_comm=orig_comm.replace(')', '.*')
			#orig_comm=orig_comm.replace('=', '.*')
			#orig_comm=orig_comm.replace('>', '.*')
			#orig_comm=orig_comm.replace('#', '.*')
			#orig_comm=orig_comm.replace(',', '.*')			
			#orig_comm=orig_comm.replace(';', '.*')
			#orig_comm=orig_comm.replace('$', '.*')
			#orig_comm=orig_comm.replace('&', '.*')
			#orig_comm=orig_comm.replace(':', '.*')
			#orig_comm=orig_comm.replace('"', '.*')
			
			for commanda in orig_comm.split('\n'):
				print 'DEL orig_comm %s' % commanda
				comm="sed -i '/%s/d' %s" % (commanda, file_name)
				self._exe_ssh(comm)
			return True
			
		if flag.find('-#!/')>=0:
			file_name=flag.replace('-#!', '')
			insert_string=None
			
			print 'file_name %s' % file_name
			
			if file_name.find('#')>0:
				cool=file_name.split('#')
				file_name=cool[0]
				insert_string=cool[1]
				
			orig_comm=orig_comm.replace(flag+'\n', '')
			orig_comm=orig_comm.replace('\t', '')
			#orig_comm=orig_comm.replace('\n\n', '')
			orig_comm=orig_comm.replace(';', '\;')
			orig_comm=orig_comm.replace('/', '\/')
			#orig_comm=orig_comm.replace('#', '\#')
			
			str_arr=[]
			for c in orig_comm.split('\n'):
				if c:str_arr.append(c)
				
			if len(str_arr)>1:
				cut_start=str_arr[0]
				#TODO Clean empty ROW
				cut_end=str_arr[-1]
				print 'original comm'
				print orig_comm
				print 'block arr %s' % str(str_arr)
				print 'cut_start %s' % cut_start
				print 'cut_end %s' % cut_end
				
				comm="sed -i '/%s/,/%s/d' %s" % (cut_start, cut_end, file_name)
			else:
				comm="sed -i '/%s/d' %s" % (str_arr[0], file_name)
				
			self._exe_ssh(comm)
			return True
		
		if flag.find('#!/')>=0 :
			file_name=flag.replace('#!', '')
			insert_string=None
			
			print 'file_name %s' % file_name
			
			if file_name.find('#')>0:
				cool=file_name.split('#')
				file_name=cool[0]
				insert_string=cool[1]
				
			orig_comm=orig_comm.replace(flag+'\n', '')
			orig_comm='\\'+orig_comm
			orig_comm=orig_comm.replace('\n', '\\n')
			orig_comm=orig_comm.replace(';', '\;')
			orig_comm=orig_comm.replace('\t', '')
			#orig_comm=orig_comm.replace('*', '\*;')
			print 'orig_comm %s' % orig_comm
			
			if insert_string:
				comm="sed -i '/%s/a %s' %s" % (insert_string, orig_comm, file_name)
			else:
				comm="sed -i '$ a %s' %s" % (orig_comm, file_name)
			self._exe_ssh(comm)
			
			return True