# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################
import shutil
import os
import polib

import xml.etree.ElementTree as ET
from api import base_api


class clean_distrib(base_api):
	def __init__(self, path, source_path):
		
		base_api.__init__(self)
		
		if path[-1:]!='/':
			path=path+'/'
			
		self.dest_path=path
		self.procc_dist_path=path
		self.source_path=source_path

		self.bad_po_in_disrib=[]
		self.bad_po_in_etalon=[]
		
		self.addons_arr=['account']
		#self._get_addons_arr()
		
		#self.copy_trans()
		
		print 'bad_po_in_disrib'
		print self.bad_po_in_disrib
		print 'bad_po_in_etalon'
		print self.bad_po_in_etalon
	
	def copy_trans(self):
		for dir in self.addons_arr:
			print dir

			dest_po_file=self.dest_path+dir+'/i18n/ru.po'
			source_po_file=self.source_path+dir+'/i18n/ru.po'
			
			po = polib.pofile(dest_po_file)
			print dest_po_file
			print 'Translate po perscent before'
			po.percent_translated()
			
			cmd='msgcat --use-first --output-file=%s %s %s' % (dest_po_file, source_po_file, dest_po_file)
			print cmd
			
			self.exe_local(cmd)
			
			po = polib.pofile(dest_po_file)
			print 'Translate po perscent before'
			po.percent_translated()
			
			#print dest_po_file
			#print source_po_file
		
	def _get_addons_arr(self):
		#print self.dest_path
		self.addons_arr=[]
		for curr in os.walk(self.dest_path):
			
			meksa=curr[0].replace(self.dest_path,'').split('/')
			#print meksa
			if len(meksa)==1 and meksa[0]:
				dir=meksa[0]
				dest_po_file=self.dest_path+dir+'/i18n/ru.po'
				source_po_file=self.source_path+dir+'/i18n/ru.po'
				
				if not os.path.isfile(dest_po_file):
					self.bad_po_in_disrib.append(dir)
					continue
				
				if not os.path.isfile(source_po_file):
					self.bad_po_in_etalon.append(dir)
					continue
				
				self.addons_arr.append(dir)
				
		print self.addons_arr
	#Private	
	def _del_po_file(self, root, f):
		if f[-3:]=='.po' and f!='ru.po' and f!='be.po' and root[-4:]=='i18n':
			fname=root+'/'+f
			print fname
			os.remove(fname)
	#Private		
	def _del_intern_dir(self, root):
		curr_dir=root.split('/')[-1:][0]
		if curr_dir.find('l10n_')>=0 and curr_dir!='l10n_ru' and curr_dir!='l10n_be':
			print root
			shutil.rmtree(root,  ignore_errors=True)
			
	def del_unnecessary_files(self, root):
		del_arr=['account_anglo_saxon',
				''
				]
					
	def del_po(self):
		files = os.listdir(self.procc_dist_path)
		
		for root, dirnames, filenames in os.walk(self.procc_dist_path):
			for f in filenames:
				self. _del_po_file(root, f)
				self._del_intern_dir(root)
				
	def remove_node_from_xml(self, path, node_id):
		file_path=self.procc_dist_path+'/'+path
		print file_path
		tree = ET.parse(file_path)
		root = tree.getroot()

		#tree.remove(tree.findall(".//record[@id='%s']" % node_id)[1])
		to_del_node=root.findall(".//record[@id='%s']" % node_id)
		if to_del_node:
			to_del_node=to_del_node[0]
			print to_del_node.text
			root.remove(to_del_node)
		#	#tree.write(file_path)
		else:
			print 'Not found record with id=%s' % node_id
			return False

	def get_stats(self):
		for dir in self.addons_arr:
			print dir
			f=self.dest_path+dir+'/i18n/ru.po'
			po = polib.pofile(f)
			print po.percent_translated()
			#for entry in po:
			#	
			#	print entry.msgid, entry.msgstr
			
cd=clean_distrib('/mnt/Notebook/opt/odoo-master/openerp/addons/', '/opt/openerp/server7/openerp/addons/')	
cd.fs_storage_path='/opt/odoo-master/'
cd.get_stats()
#cd.remove_node_from_xml('base/module/module_view.xml', 'modules_act_cl')
#ssh root@192.168.1.110 sudo /etc/init.d/openerp-server stop
#sudo su - openerp -s /bin/bash
#/opt/odoo-master/openerp-server  -c /etc/openerp-server.conf
#cd.del_po()
cd.copy_trans()
#cd.change_access_mode()
	