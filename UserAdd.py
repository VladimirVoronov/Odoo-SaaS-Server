# -*- encoding: utf-8 -*-

##############################################################################
#
#
##############################################################################

import os
import re
import shutil
import polib
import ConfigParser
import logging

from ConfigParser import SafeConfigParser
from UserCommon import UserCommon

#from api import base_api

#$ Install Notes
	
#/etc/postfix/alias_maps
#/etc/aliases
#/opt/mailgate/openerp_mailgate.py

#class myodoo_register(base_api):

class myodoo_register(UserCommon):
	
	def _print_attr(self):
		logging.info('*'* 50)
		logging.info('User name %s' % self.account)
		logging.debug('*'* 50)
		logging.debug('Extens vals')
		logging.debug('*'* 50)
		
		for curr in self.__dict__:
			val=self.__dict__[curr]
			val=val.replace(self.abonent_pass, '*****')
			val=val.replace(self.user_pass, '*****')
			logging.debug('%s = %s' % (curr, val))
			
		logging.debug('*'* 50)
				
	def __init__(self):
		self.read_config()
		self.command_prefix=''
		
		logging.basicConfig(filename=self.log_file, level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
		logging.info('Init User Add')
		
	def init_vals(self):
		self.add_user_comm="""#!sh
		useradd --create-home -s /dev/null { account }
		usermod -a -G { account } root
		usermod -a -G { account } myodoo
		usermod -a -G { account } asterisk
		
		mkdir { record_dir }
		chown asterisk:asterisk { record_dir }
		chmod 770 { record_dir }
		
		mkdir { backup_dir }
		chown root:root { backup_dir }
		chmod 770 { backup_dir }
		""" 
		
		self.add_alias1="""#!/etc/postfix/alias_maps
		@{ account }.{ root_domain } { account }@my.{ root_domain }
		"""
		self.add_alias2="""#!/etc/aliases
		{ account }: \"|/opt/mailgate/openerp_mailgate.py  --user=1  --port=9080 --password={ user_pass } --host=localhost -d { account }\"
		"""
		self.add_resresh_post="""#!sh
		postmap /etc/postfix/alias_maps
		newaliases
		"""
		self.add_db="""#!sh
		createdb  -O myodoo  -w { account }
		pg_restore -Fc -n public --no-owner -d { account }  --role myodoo { db_etalon_path }
		"""
		self.add_sql=u"""#!SQL
		UPDATE base_config_settingsITS CLEAN SET alias_domain='{ account }.{ root_domain }'
		
		UPDATE ir_config_parameter SET value='{ account }.{ root_domain }' WHERE key='mail.catchall.domain'
		UPDATE ir_config_parameter SET value='{ uuid }' WHERE key='database.uuid'
		INSERT INTO ir_config_parameter(value,  key) VALUES ('db', 'ir_attachment.location')
		
		UPDATE res_partner SET country_id=192, display_name='{ user_company }', name='{ user_company }' WHERE id={ db_company_id }
		
		UPDATE res_partner SET mobile='{ user_phone }', email='{ user_email }', display_name='{ user_name } ', name='{ user_name }' WHERE id={ db_user_id }
		
		UPDATE res_partner SET tz='Europe/Moscow'
		
		INSERT INTO asterisk_server (out_prefix, active,  password, ip_address, port, name, alert_info,  company_id,  wait_time, context, login, extension_priority) VALUES ('', true,  '{ ami_pass }', '{ ami_host }', { ami_port }, 'myAsterisk', NULL,  1, 90, 'openerp_callback', '{ ami_login }', 1)
		
		UPDATE res_users SET   password='{ user_pass }', login='{ user_email }', asterisk_server_id=1, asterisk_chan_type= 'SIP', resource='{ abonent_phone }', internal_number='{ abonent_phone }', callerid='CallbackRobot <{ abonent_phone }>' WHERE id=1
				
		UPDATE res_company SET name='{ user_company }',  email='admin@{ account }.{ root_domain }',  phone='{ trunk_phone } ext. { abonent_phone }', currency_id=31 WHERE id=1
		
		"""
		#INSERT INTO fetchmail_server (out_prefix, active,  password, ip_address, port, name, alert_info,  company_id,  wait_time, context, login, extension_priority) VALUES ('0', true,  '{ ami_pass }', '{ ami_host }', { ami_port }, 'myAsterisk', NULL,  1, 90, 'openerp_callback', '{ ami_login }', 1)
	
		#notify_email='always',
		#INSERT INTO asterisk_server (out_prefix, active,  password, ip_address, port, name, alert_info,  company_id,  wait_time, context, login, extension_priority) VALUES ('0', true,  '1234', 'localhost', 5038, 'myAsterisk', NULL,  1, 90, 'openerp_callback', 'click2dial', 1)
		#####self.default_abonent_context='CONTEXT ???????'
		
		self.add_sip="""#!/etc/asterisk/sip.conf
		;START Gegister phone { abonent_phone }
		[{ abonent_phone }]
		nat=force_rport,comedia
	 	qualify=300  
		secret={ abonent_pass }
		type = peer
		host=dynamic
		context = { default_abonent_context }
		disallow = all
		allow = ulaw,alaw,g729
		;END Gegister phone { abonent_phone }
		"""
		self.root_port='8069'
		self.add_extension2="""#!/etc/asterisk/extensions.conf#;aaa Robot 2 aaa
		;START AUTO DIALPLAN2 { abonent_phone }
		exten => { abonent_phone },1,Set(call_id=${EPOCH})
		exten => { abonent_phone },n,MixMonitor(/home/{ account }/phone_records/${call_id}.wav)
		exten => { abonent_phone },n,Dial(SIP/{ abonent_phone },60,rg))
		exten => { abonent_phone },n,System(wget "{ account }.{ root_domain }:9080/phones/?call_id=${call_id}&phone=${CALLERID(num)}&user_id={ abonent_phone }&type=in&call_state=${DIALSTATUS}&duration=${CDR(duration)}")
		
		exten => { abonent_phone },n,Hangup
		;END AUTO DIALPLAN2 { abonent_phone }
		"""

		self.add_extension1="""#!/etc/asterisk/extensions.conf#;aaa Robot 1 aaa
		;START AUTO DIALPLAN1 { abonent_phone }
		exten => { abonent_phone },1,Set(call_id=${EPOCH})
		exten => { abonent_phone },n,MixMonitor(/home/{ account }/phone_records/${call_id}.wav)
		exten => { abonent_phone },n,Dial(SIP/30224,60,rg))
		exten => { abonent_phone },n,System(curl "http://{ account }.{ root_domain }:9080/phones/?call_id=${call_id}&call_state=${DIALSTATUS}&duration=${CDR(duration)}")
		;END AUTO DIALPLAN1 { abonent_phone }
		"""
				
		self.add_resresh_sip="""#!sh
		asterisk -rx "reload"
		"""

		self.hosts="""#!/etc/hosts
		127.0.0.1 { account }.{ root_domain }
		"""
		self.add_confirm="""#!sh
		wget http://www.myodoo.ru:9080/base_ready/{ account } > /dev/null
		"""		
	def add_user(self):
		self._print_attr()
		self.init_vals()
		
		self.exe(self.add_user_comm)
		self.exe(self.add_alias1)
		self.exe(self.add_alias2)
		self.exe(self.add_resresh_post)
		self.exe(self.add_db)
		self.exe(self.add_sql)
		
		self.exe(self.add_sip)
		self.exe(self.add_extension1)
		self.exe(self.add_extension2)
		self.exe(self.add_resresh_sip)

		self.exe(self.hosts)
		
		self.print_sip_info()
		
		self.exe(self.add_confirm)
		
	def print_sip_info(self):
		print '='*20
		print 'SIP account'
		print 'sip:%s@192.168.1.110' % self.abonent_phone
		print self.abonent_pass
		print '='*20
	
	def print_odoo_info(self):
		print '='*20
		print 'http://%s.myodoo.ru/' % self.account
		print 'DB email=%s' % self.user_email
		print 'DB user pass-%s' % self.user_pass
		print '='*20				
