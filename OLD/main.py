# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################
from api import base_api

class prepare_system(base_api):
	def main(self):
		self.update_system()
		
		comm=[
		'apt-get install -y  postgresql',
		'apt-get install -y  iptables-persistent',
		 
		"echo 'net.ipv4.ip_forward = 1' >>/etc/sysctl.conf",
		'sysctl -p /etc/sysctl.conf',
		'iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8069',
		'iptables -P FORWARD ACCEPT',

		
		'iptables -I INPUT 1 -i lo -j ACCEPT',
		'iptables -A INPUT -p tcp -m tcp --tcp-flags ACK ACK -j ACCEPT',
		'iptables -A INPUT -m state --state ESTABLISHED -j ACCEPT',
		'iptables -A INPUT -m state --state RELATED -j ACCEPT',
		'iptables -A INPUT -p udp --dport 53 -j ACCEPT',
		'iptables -A INPUT -p tcp --destination-port 22 -j ACCEPT'
		'service iptables-persistent save'
		
		"echo 'pre-up iptables-restore < /etc/iptables.rules' >>/etc/network/interfaces",
		"echo 'post-down iptables-save -c > /etc/iptables.rules' >>/etc/network/interfaces"]

		self.exe_command(comm)
		
class install_openerp(base_api):
	def __init__(self):
		postres_ver='9.1'
		self.pg_acc_file='/etc/postgresql/%s/main/pg_hba.conf' % postres_ver
		self.local_openerp_storage='/opt/openerp/server7/'
	
	def install_libs(self):
		self.update_system()
		comm=[
		'apt-get install -y  python-psycopg2 python-simplejson python-lxml  python-pydot python-tz python-requests',
		'apt-get install -y  python-yaml python-reportlab python-mako python-pychart',
		'apt-get install -y  python-werkzeug python-pybabel python-dateutil python-openid',
		'apt-get install -y  python-serial python-pytils postgresql python-xlrd  python-xlwt',
		'apt-get install -y  zip python-psutil python-jinja2 python-pip mercurial python-unittest2',
		'apt-get install -y  python-mock python-docutils python-setuptools python-asterisk postgresql',
		'apt-get install -y  postfix']
		
		self.exe_command(comm)
		
	def install_folders(self):
		comm=[
		'adduser --system --group openerp',
		#'sysctl -w net.ipv4.ip_forward=1'
		"echo 'net.ipv4.ip_forward = 1' >>/etc/sysctl.conf",
		'sysctl -p /etc/sysctl.conf',
		'iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8069',
		'sudo iptables -P FORWARD ACCEPT',
		
		'iptables -I INPUT 1 -i lo -j ACCEPT',
		'iptables -A INPUT -p tcp -m tcp --tcp-flags ACK ACK -j ACCEPT',
		'iptables -A INPUT -m state --state ESTABLISHED -j ACCEPT',
		'iptables -A INPUT -m state --state RELATED -j ACCEPT',
		'iptables -A INPUT -p udp --dport 53 -j ACCEPT',
		'iptables -A INPUT -p tcp --dport 22 -j ACCEPT',
		
		'touch /etc/iptables.rules',
		"echo 'pre-up iptables-restore < /etc/iptables.rules' >>/etc/network/interfaces",
		"echo 'post-down iptables-save -c > /etc/iptables.rules' >>/etc/network/interfaces",

		'mkdir -p /var/log/openerp',
		'mkdir -p /var/run/openerp',
		'mkdir -p /opt/openerp/server',
		'mkdir -p /opt/openerp/myaddons',
		'mkdir -p /opt/db_image',
		
		'chown -R openerp:root /var/log/openerp',
		'chown -R openerp:root /var/run/openerp',
		'chown -R root:openerp /opt/openerp/',

		'chmod -R 770 /var/log/openerp',
		'chmod -R 770 /var/run/openerp',
		'chmod -R 770 /opt/openerp/',
		'chmod -R 770 /opt/db_image']
		
		self.exe_command(comm)
		
	def fill_files(self):
		#self.local_openerp_storage
		pass
		
	def copy_files(self):
		self.copy_file('openerp-server.conf', '/etc/')
		self.copy_file('openerp-server', '/etc/init.d/')
		
		comm=[
			'chmod +x /etc/init.d/openerp-server',
			'update-rc.d openerp-server start 70 2 3 4 5 . stop 20 0 1 6 .'
			]
		
		self.exe_command(comm)
		
	def prepare_postfix(self):
		self.copy_file('main.cf', '/etc/postfix/')
		
		comm=[
			'touch /etc/postfix/alias_maps',
			
			'chown root:root /etc/postfix/alias_maps',
			'chown root:root /etc/postfix/main.cf',
			
			'chmod 774 /etc/postfix/alias_maps',
			'chmod 774 /etc/postfix/main.cf',
			
			'/etc/init.d/postfix reload',
			'mkdir /opt/mailgate/',

			]
			
		self.exe_command(comm)
		self.copy_file('openerp_mailgate.py', '/opt/mailgate/')
		
		comm=[
			'chown root:postfix -R  /opt/mailgate/',
			'chmod 774 -R /opt/mailgate/',
			'chmod +X /opt/mailgate/openerp_mailgate.py',
			
			'touch /etc/postfix/alias_maps',
						
			'chown root:postfix /etc/postfix/alias_maps',
			'chown root:postfix /etc/postfix/main.cf',
			
			'chmod 774 /etc/postfix/alias_maps',
			'chmod 774 /etc/postfix/main.cf',
			
			'/etc/init.d/postfix reload'
			]
		
		self.exe_command(comm)
		
	def posgtres(self):

		#self.exe_command('rm %s'% acc_file)
		
		self.add_row_to_file(self.pg_acc_file, 'local all postgres trust')
		self.add_row_to_file(self.pg_acc_file, 'local all openerp peer')
		self.add_row_to_file(self.pg_acc_file, 'local all root peer')
		self.add_row_to_file(self.pg_acc_file, 'host all root 127.0.0.1/32 trust')
		
		self.exe_command('/etc/init.d/postgresql restart')
		
		self.exe_command('/usr/bin/createuser --createdb --username postgres --no-createrole --no-superuser openerp')
		self.exe_command('/usr/bin/createuser --createdb --username postgres --createrole --superuser root')
		
		#Check acees for other users WARNING
		self.add_log('Local Connect over SSH tunel user root')
		self.add_log('ssh -f -N -L 3832:127.0.0.1:5432 %s@%s' % (self.user, self.host))
		
		self.add_log('Remote SSH debug over openerp user')
		self.add_log('ssh %s@%s'% (self.user, self.host))
		self.add_log('su - openerp -s /bin/bash')
		self.add_log('/opt/openerp/server/openerp-server  -c /etc/openerp-server.conf')
		
class add_account(base_api):
	def __init__(self, account):
		self.account=account
		self.etalon_path='/opt/db_image/etalon.backup'
		
	def add_post_domain(self):
		self.exe_command('useradd -s /dev/null %s' % self.account)
		self.add_row_to_file('/etc/postfix/alias_maps', '@%s.my.arterp.sru %s@localhost' % (self.account, self.account))
		self.add_row_to_file('/etc/aliases', """%s: "|/opt/mailgate/openerp_mailgate.py --model=mail.message --host=localhost --port 8069 -d %s" """ % (self.account, self.account))
		
		comm=[
			'postmap /etc/postfix/alias_maps',
			'newaliases',
			]
		
		self.exe_command(comm)
		
	def restore_from_dump(self):
		self.exe_command('createdb  -O openerp  -w %s' % self.account)
		
		comm="pg_restore -F t --no-owner  -d %s  --role openerp %s" % (self.account, self.etalon_path)
		self.exe_command(comm)

	def exe_sqls(self):
		sql="INSERT INTO ir_config_parameter(key, value) VALUES ('apps.server', 'localhost ');"
		self.exe_sql(sql)
		
class clean_distrib(base_api):
	def __init__(self):
		pass
	
	def install_libs(self):
		self.update_system()
		comm=[
		'apt-get install -y  g++ ncurses-dev  build-essential libxml2-dev curl',
		'apt-get install -y  sqlite3 libsqlite3-dev postgresql libpq-dev subversion',
		'postgresql']
		
		self.exe_command(comm)
		
	def install_asterisk(self):
		version=11
		comm=[
		'wget http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-11-current.tar.gz' % version,
		'tar -xzf asterisk-%d-current.tar.gz' % version,
		'cd asterisk-11.2.0',
		'./configure --with-postgres']
		
		#make menuselect
		#make
		
		self.exe_command(comm)

	def posgtres(self):
		self.exe_command('/usr/bin/createuser --createdb --username postgres --no-createrole --no-superuser asterisk')

		self.add_row_to_file(self.pg_acc_file, 'local asterisk asterisk peer')
		
		self.exe_command('/etc/init.d/postgresql restart')
		self.exe_command('createdb  -O asterisk  -w asterisk')