# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################

from UserCommon import UserCommon
#For notebook
#echo 'HandleLidSwitch=ignore' >>/etc/systemd/logind.conf
#restart systemd-logind

class SystemInstall(UserCommon):
	def __init__(self):
		self.ssh_user='root'
		self.ssh_host='192.168.1.110'
		
		debug="""
		netstat -ltupn
		"""
		self.manual1="""#!Manual
		scp  ~/.ssh/id_dsa.pub vovan@10.0.0.100:/tmp/
		
		login
		ssh vovan@10.0.0.100
		sudo sh -c 'mkdir /root/.ssh/'
		sudo sh -c 'touch /root/.ssh/authorized_keys2'
		sudo sh -c 'cat /tmp/id_dsa.pub |  cat - >> /root/.ssh/authorized_keys2'
		sudo sh -c 'chown -R root:root /root/.ssh/'
		sudo sh -c 'sudo chmod 600 /root/.ssh/authorized_keys2'
		sudo sh -c 'sudo chmod 755 /root/ /root/.ssh/'
		sudo sh -c 'cat /root/.ssh/authorized_keys2'
		
		sudo sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
		sudo sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config
		sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
		
		sudo service ssh restart
		
		ssh root@10.0.0.100
		
		apt-get update
		sudo dpkg-reconfigure tzdata
		"""
		install_postfix="""#!sh
		apt-get install -y  postfix
		apt-get install opendkim opendkim-tools
		
		mkdir /etc/opendkim/
		
		touch /etc/postfix/alias_maps
		
		mkdir -p /opt/mailgate
		copy /opt/mailgate/openerp_mailgate.py
		chmod 755 -R /opt/mailgate/
		
		copy /etc/postfix/main.cf
		
		/etc/init.d/postfix restart
		
		"""
		install_libs="""#!sh
apt-get install -y  python-psycopg2 python-simplejson python-lxml  python-pydot python-tz python-requests
apt-get install -y  python-yaml python-reportlab python-mako python-pychart
apt-get install -y  python-werkzeug python-pybabel python-dateutil python-openid
apt-get install -y  python-serial python-pytils postgresql python-xlrd  python-xlwt
apt-get install -y  zip python-psutil python-jinja2 python-pip mercurial python-unittest2
apt-get install -y  python-mock python-docutils python-setuptools python-asterisk
apt-get install -y  python-decorator python-pyPdf python-passlib python-polib  python-ldap
apt-get install -y  python-pip curl pgpgpg xfonts-base xfonts-75dpi postgresql  wkhtmltopdf xvfb

#
apt-get install -y  node-less
sudo apt-get install nodejs
sudo apt-get install npm
sudo npm install -g less
sudo npm install -g less-plugin-clean-css
sudo ln -s /usr/local/bin/lessc /usr/bin/lessc
sudo ln -s /usr/bin/nodejs /usr/bin/node

		pip install phonenumbers traceback2
		
		apt-get install  xfonts-75dpi xvfb

		#http://wkhtmltopdf.org/downloads.html
		wget http://download.gna.org/wkhtmltopdf/0.12/0.12.2.1/wkhtmltox-0.12.2.1_linux-trusty-i386.deb
		sudo dpkg -i /tmp/wkhtmltox-0.12.2.1_linux-trusty-i386.deb

sudo -i
mv /usr/bin/wkhtmltopdf /usr/bin/wkhtmltopdf-origin
touch /usr/bin/wkhtmltopdf && chmod +x /usr/bin/wkhtmltopdf && cat > /usr/bin/wkhtmltopdf << END
#!/bin/bash

/usr/bin/xvfb-run -a -s "-screen 0 1024x768x24" /usr/local/bin/wkhtmltopdf  "\$@"
END

    Download and uncompress in /usr/lib/python2.7/dist-packages/reportlab/fonts these file

    http://www.reportlab.com/ftp/fonts/pfbfer.zip


		#Then in /etc/init.d/openerp-server add  /usr/local/bin to the front of path environment variable, e.g.
		#PATH=/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
		#cd /tmp
		
		"""
		hba_conf="""
		local   all             postgres                                peer
		local   all             odoo                                	peer
		local   all             root                                	peer
		#
		host    all             root             127.0.0.1/32           trust
		
		/etc/init.d/postgresql restart

		sudo -u postgres psql template1
		createuser --createdb --username postgres --no-createrole --no-superuser  odoo;
		createuser --createdb --username postgres --createrole --superuser --replication  root;
		

		alter role odoo with superuser;
		alter role root with superuser;
		

		"""
		asterisk_debug="""
		http://habrahabr.ru/post/207934/
		http://www.voip-info.org/wiki/view/Asterisk+modules
		
		/etc/astrisk modules
		Pered Global
		;  Channels --
		noload => chan_mgcp.so           ; Media Gateway Control Protocol (MGCP) - Requires res_features.so
		noload => chan_skinny.so         ; Skinny Client Control Protocol (Skinny) - Requires res_features.so
		noload => chan_unistim.so         ; Unistim control protocol
		noload => chan_iax.so
		noload => chan_iax2.so
		noload => pbx_dundi.so
		
		/etc/init.d/asterisk restart
		"""
		
		asterisk_copy="""#!LocalCopy
		/etc/asterisk/sip.conf
		/etc/asterisk/extensions.conf
		/etc/asterisk/manager.conf
		"""
		asterisk_sh="""#!sh
		chown asterisk:asterisk /etc/asterisk/sip.conf
		chown asterisk:asterisk /etc/asterisk/extensions.conf
		chown asterisk:asterisk /etc/asterisk/manager.conf
		
		Russian sound Asterisk path
		/usr/share/asterisk/sounds/ru_RU_f_IvrvoiceRU
		
		/etc/init.d/asterisk restart
		asterisk -rx "reload"
		asterisk -rx "module reload manager"
		"""
		
		install_network="""#!sh
		in /etc/default/grub
		именить строку
		GRUB_CMDLINE_LINUX="ipv6.disable=1"
		
		sudo update-grub
		sudo update-grub2
		
		????apt-get install iptables-persistent
		
		echo 'net.ipv4.ip_forward = 1' >>/etc/sysctl.conf
		

		iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 9080
		
		???iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 9080
		
		iptables -P FORWARD DROP


		############
		apt-get install iptables-persistent

		sudo /etc/init.d/iptables-persistent save
        sudo /etc/init.d/iptables-persistent reload
        ############

		"""
		
		myodoo_copy="""#!LocalCopy
		/etc/myodoo.conf
		/etc/init.d/myodoo
		"""
		
		install_myodoo="""#!sh

		adduser --system --group odoo
		
		usermod -a -G odoo root
		usermod -a -G syslog odoo
		
		mkdir /home/myodoo/phone_records/
		
		mkdir -p /var/log/odoo
		mkdir -p /var/run/odoo
		
		mkdir -p /opt/odoo/odoo
		mkdir -p /opt/odoo/addonsodoo


		chown -R odoo:odoo /var/log/odoo
		chown -R odoo:odoo /var/run/odoo
		chown -R odoo:odoo /opt/odoo/

		chmod -R 770 /var/log/odoo
		chmod -R 770 /var/run/odoo
		chmod -R 770 /opt/odoo/

		update-rc.d odoo defaults
		"""
		
		myodoo_manual="""#!Manual
		#debug
		sudo su - myodoo -s /bin/bash
		cd /opt/myodoo/myodoo/
		/opt/myodoo/myodoo/openerp-server  -c /etc/myodoo.conf
		"""
		dns="""
		dnssec-keygen -a HMAC-MD5 -b 128 -r /dev/urandom -n USER DHCP_UPDATER
		cat Kdhcp_updater.*.private|grep Key
		mkdir /etc/resolvconf/resolv.conf.d
		touch /etc/resolvconf/resolv.conf.d/tail

		"""
si=SystemInstall()