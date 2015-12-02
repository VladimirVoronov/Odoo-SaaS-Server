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
from api import base_api

class prep_distrib(base_api):
	def __init__(self, source_path, dest_path):
		base_api.__init__(self)
		
		self.source_path=source_path
		self.dest_path=dest_path
		
		self.bad_po_in_disrib=[]
		self.bad_po_in_etalon=[]
		
		#self.copy_trans()
		
		print 'bad_po_in_disrib'
		print self.bad_po_in_disrib
		print 'bad_po_in_etalon'
		print self.bad_po_in_etalon
		
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
					
	def del_po(self, path):
		#files = os.listdir(self.procc_dist_path)
		
		for root, dirnames, filenames in os.walk(path):
			for f in filenames:
				self. _del_po_file(root, f)
				self._del_intern_dir(root)
	
	def merge_translate(self, module, source_path, dest_path):
		
		dest_po_file=dest_path+module+'/i18n/ru.po'
		source_po_file=source_path+module+'/i18n/ru.po'
		
		if not os.path.isfile(dest_po_file):
			self.bad_po_in_disrib.append(dir)
			return False
		
		if not os.path.isfile(source_po_file):
			self.bad_po_in_etalon.append(dir)
			return False
		
		po = polib.pofile(dest_po_file)
		print 'Translate po perscent before %d' % po.percent_translated()
		
		
		cmd='msgcat --use-first --output-file=%s %s %s' % (dest_po_file, source_po_file, dest_po_file)
		
		self.exe_local(cmd)
		
		po = polib.pofile(dest_po_file)
		print 'Translate po perscent before %d' % po.percent_translated()
		
		
		print dest_po_file
		print source_po_file
		
	def get_modules_arr(self, mask=False):
		ret_arr=[]
		for curr in os.walk(self.source_path):
			meksa=curr[0].replace(self.source_path,'').split('/')
			if len(meksa)==1 and meksa[0]:
				module=meksa[0]
				if mask:
					if meksa[0].find(mask)>=0:
						ret_arr.append(module)
				else:
					ret_arr.append(module)
				#self.procc_dic(meksa[0])
		return ret_arr
	
	def get_info_by_module(self, curr, path, path_name, print_info=True):
		
		po_file_name=path+curr+'/i18n/ru.po'
		
		
		if not os.path.isfile(po_file_name):
			#print "ERROR file dont found- %s" % po_file_name
			return False, False
			
		po = polib.pofile(po_file_name)
		#if po.percent_translated()==100: return True
		if print_info:
			print "Percent translate %s= %d" % (path_name, po.percent_translated())
			print "Total UNTRANSLATED items %s= %d" % (path_name, len(po.untranslated_entries()))
			print "Total items %s= %d" % (path_name, len(po))
			print "Last-Translator %s= %s" % (path_name, po.metadata['Last-Translator'])
			print "*"
		return po.percent_translated(), len(po.untranslated_entries())
	
	def print_info1(self):
		count=0
		untrans_items=0
		#for curr in self.get_modules_arr(mask='crm'):
		
		exclude_list=['website_gengo',
					'base_gengo',
					'account_check_writing',
					'point_of_sale',
					]
		for curr in self.get_modules_arr():
		
			path1='/opt/openerp/server7/openerp/addons/'
			path2='/opt/openerp/alpha/addons/'
			path3='/opt/openerp/master/addons/'
			path4='/opt/openerp/saas8/addons/'
			path5='/opt/openerp/karat/'
			
			path6='/opt/openerp/addons_collex'
			path7='/opt/openerp/odoo-master/addons'
			
			#escape if 100%
			#get_info_by_module return percent value
			#if self.get_info_by_module(curr, '/opt/openerp/addons_collex/', "xxxx", print_info=False)==100:continue
			if curr.find('l10n_')>=0:continue
			info, untrans=self.get_info_by_module(curr, '/opt/openerp/odoo/addons/', "xxxx", print_info=False)
			if info==100:continue
			if untrans==0:continue
			if curr in exclude_list:continue
			
			print '='*30
			print curr
			
			self.get_info_by_module(curr, '/opt/openerp/odoo/addons/', "work_8")
			self.get_info_by_module(curr, '/opt/openerp/addons_collex/', "collex")
			self.get_info_by_module(curr, '/opt/openerp/karat/', "karat")
			self.get_info_by_module(curr, '/opt/openerp/saas8/addons/', "saas_8")
			
			# Merge with etalon
			#self.merge_translate(curr, '/opt/openerp/odoo-master/', '/opt/openerp/odoo/addons/')
			
			#################################################################################
			# Merge with my
			#self.merge_translate(curr, '/opt/openerp/server7/openerp/addons/', '/opt/openerp/odoo/addons/')
			#Merge with karat
			#self.merge_translate(curr, '/opt/openerp/karat/', '/opt/openerp/odoo/addons/')
			#Merge with collex
			#self.merge_translate(curr, '/opt/openerp/addons_collex/', '/opt/openerp/odoo/addons/')
			# Merge with Saas8
			#self.merge_translate(curr, '/opt/openerp/saas8/addons/', '/opt/openerp/odoo/addons/')
			
			#self.get_info_by_module(curr, path2, "7 distrib")
			#self.get_info_by_module(curr, path3, "master")
			#self.get_info_by_module(curr, path4, "saas")
			#self.get_info_by_module(curr, path5, "karat")
			
			#self.get_info_by_module(curr, path6, "collex 8")
			#self.get_info_by_module(curr, path7, "master 8")
			
			count+=1
			untrans_items+=untrans
		print count
		print untrans_items
		
pd=prep_distrib('/opt/openerp/odoo-master/addons/', '/opt/openerp/odoo2/addons')
#pd.del_po('/opt/openerp/addons_collex/')

arr=pd.print_info1()
#pd.get_info_by_module('account', '/opt/openerp/odoo-master/addons/', "my work")

#pd=prep_distrib('/opt/openerp/server7/openerp/addons/', '/mnt/Notebook/opt/openerp/server/openerp/addons/')

#pd.del_po('/opt/openerp/saas8/addons/')

path1='/opt/openerp/server7/openerp/addons/ change path!!!!!!!!!!! server7_my_main_save_error'
path2='/opt/openerp/alpha/addons/'
path3='/opt/openerp/master/addons/'
path4='/opt/openerp/saas8/addons/'
			
#pd.merge_translate('crm_claim', path1, path4)
#print arr
#pd.procc_dic('crm')
#/mnt/Notebook/opt/openerp/server/openerp/addons/account/i18n/ru.po /opt/openerp/server7/openerp/addons/account/i18n/ru.po
