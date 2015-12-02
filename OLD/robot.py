# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################

import os

import shutil
import polib

from api import base_api

class myodoo(base_api):
	def __init__(self):
		self.trans_addons_path='/opt/openerp/odoo_trans/addons/'
		self.branch_addons_path='/opt/openerp/odoo2/addons/'
		self.debug_mode=False
		
	def _exe_command(self, com):
		pass
	
	def _get_po_list(self, path):
		ret_arr=[]
		for curr in os.walk(path):
			meksa=curr[0].replace(path,'').split('/')
			if len(meksa)==1 and meksa[0]:
				dir=meksa[0]
				#if dir.find('l10n_')!=-1 and dir.find('hw_')!=-1:
				
				stop_list=['l10n_', 'hw_', 'test_']
				for c in stop_list:
					if dir.find(c)>=0:
						continue

				print dir							
				ret_arr.append(dir)
		return ret_arr
	

	def copy_trans(self):
		pl=self._get_po_list(self.trans_addons_path)
		
		for dir in pl:
			dest_po_file=self.branch_addons_path+dir+'/i18n/ru.po'
			source_po_file=self.trans_addons_path+dir+'/i18n/ru.po'
			
			if not os.path.exists(source_po_file):
				print 'Error- source dont found skiped %s ' % source_po_file
				continue
			
			cmd='msgcat --use-first --output-file=%s %s %s' % (dest_po_file, source_po_file, dest_po_file)
	
			if not os.path.exists(dest_po_file) and os.path.exists(source_po_file):
				cmd='cp %s %s' % (source_po_file, self.branch_addons_path+dir+'/i18n/')
			
			if self.debug_mode:
				print cmd		
			
			res=self.exe_local(cmd)
			
			if self.debug_mode:
				print dir
				
			if res!=0:
				print 'Error exe command'
				print cmd
				print '='*20	
		print 'copy_trans DONE'
		
	def del_accupant_accounts(self):
		pl=self._get_po_list(self.branch_addons_path)
		
		for dir in pl:
			curr_dir=self.branch_addons_path+dir

			if curr_dir.find('l10n_')>=0 and curr_dir!='l10n_ru' and curr_dir!='l10n_be':
				shutil.rmtree(curr_dir,  ignore_errors=True)
				if self.debug_mode:
					print curr_dir
		print 'del_accupant_accounts DONE'		
			
	def del_modules(self):
		exclude_list=[#'website_gengo',
					#'base_gengo',
					'account_check_writing',
					#'point_of_sale',
					]
		
		for dir in exclude_list:
			curr_dir=self.branch_addons_path+dir
			#print curr_dir
			shutil.rmtree(curr_dir,  ignore_errors=True)
			
		print 'del_modules DONE'
		
	def print_run_path(self):
		pass
	
	def print_stat(self):
		pl=self._get_po_list(self.branch_addons_path)
		
		for dir in pl:
			dest_po_file=self.branch_addons_path+dir+'/i18n/ru.po'
			
			if not os.path.exists(dest_po_file):
				print 'Error- source dont found skiped %s ' % dest_po_file
				continue
			
			po = polib.pofile(dest_po_file)
			
			if len(po.untranslated_entries())==0:
				continue
			
			print 'file=%s' % dest_po_file
			print "Percent translate= %d" % po.percent_translated()
			print "Total UNTRANSLATED items= %d" % len(po.untranslated_entries())
			print "Total items= %d" % len(po)
			print "*"
			
	
md=myodoo()

#Удалить вражеские планы счетов
#md.del_accupant_accounts()

#Скопировать Русский язык с эталона в новую ветку
#md.copy_trans()

#Удалить не нужные модули
#md.del_modules()

#Печатать статистику по полученному переводу в ветке
md.print_stat()

