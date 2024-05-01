#!/usr/bin/python
# -*- coding: utf-8 -*-
###################
## ONEupdater E2 ##
###################

import os
import json
import subprocess
from os import path as os_path, remove as os_remove
from enigma import *
from datetime import datetime
from threading import Timer
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
from Plugins.Plugin import PluginDescriptor
from .extras.compat import compat_urlopen, compat_Request, PY3
from .extras.Console import Console
from .settings.Ciefp import *
from .settings.Morpheus883 import *
from .settings.Picons import *
if PY3:
    import configparser
else:
    import ConfigParser

from Components.Pixmap import Pixmap

#session = None

App = 'ONEupdater E2'
Version = '3.1'
Developer = 'Qu4k3'
ONE = 'https://sat-club.eu'
ONE_tmp =  '/tmp/ONEupdater/'
ONE_installer = 'https://raw.githubusercontent.com/Sat-Club/ONEupdaterE2/main/installer.sh'
ONE_dir = resolveFilename(SCOPE_PLUGINS, "Extensions/ONEupdater/")


def trace_error():
    import sys
    import traceback
    try:
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(file=open('/tmp/ONEupdater.log', 'a'))
    except:
        pass

def logdata(label_name = '', data = None):
    try:
        data=str(data)
        fp = open('/tmp/ONEupdater.log', 'a')
        fp.write( str(label_name) + ': ' + data +"\n")
        fp.close()
    except:
        trace_error()
        pass

def dellog(label_name = '', data = None):
    try:
        if os_path.exists('/tmp/ONEupdater.log'):
            os_remove('/tmp/ONEupdater.log')
    except:
        trace_error()
        pass


class ONEupdater(Screen):
	skin = """
    <screen title="ONEupdater E2" position="center,center" size="900,500" font="Regular;45" >
        <widget name="menu" position="30,30" size="800,400" font="Regular;25" itemHeight="45" scrollbarMode="showOnDemand" />
        <widget name="Version" position="5,475" size="100,20" font="Regular;16" halign="center" valign="center" foregroundColor="#4073ff" />
        <widget name="Developer" position="300,475" size="300,22" font="Regular;20" halign="center" valign="center" foregroundColor="#299438" />
        <widget name="Website" position="623,475" size="400,20" font="Regular;16" halign="center" valign="center" foregroundColor="#fad000" />
        <ePixmap position="310,85" size="256,256" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MyMetrix/mymetrix.png" alphatest="blend" />
    </screen>
    """

	def __init__(self, session, args = None):
		self.skin = ONEupdater.skin
		self.session = session
		Screen.__init__(self, session)
		dellog()
		logdata(App, "started")
		self.main_menu()

	def main_menu(self):
		global menu
		self.main_list = []
		self.main_list.append("Ciefp Settings")
		self.main_list.append("Morpheus883 Settings")
		self.main_list.append("Picons")
		self["menu"] = MenuList(self.main_list)
		self["Developer"] = Label(_("Developed by " + Developer))
		self["Website"] = Label(_(ONE))
		self["Version"] = Label(_("Version " + Version))

		self["actions"] = ActionMap(["OkCancelActions", "NumberActions"],{"ok": self.ok, "cancel": self.Exit}, -1)
		menu = 0
		t = Timer(0.5, self.update_me)
		t.start()

	def menu_picons(self):
		global menu
		menu = 1
		self.picons_list = []
		self.picons_list.append(Picons1)
		self.picons_list.append(Picons14)
		self.picons_list.append(Picons15)
		self.picons_list.append(Picons16)
		self.picons_list.append(Picons17)
		self.picons_list.append(Picons18)
		self.picons_list.append(Picons2)
		self.picons_list.append(Picons3)
		self.picons_list.append(Picons4)
		self.picons_list.append(Picons5)
		self.picons_list.append(Picons6)
		self.picons_list.append(Picons7)
		self.picons_list.append(Picons8)
		self.picons_list.append(Picons9)
		self.picons_list.append(Picons10)
		self.picons_list.append(Picons11)
		self.picons_list.append(Picons12)
		self.picons_list.append(Picons13)
		self["menu"].moveToIndex(0)
		self["menu"].l.setList(self.picons_list)
		self.setTitle(_(App + " > Picons"))

	def menu_ciefp(self):
		global menu
		menu = 1
		self.ciefp_list = []
		self.ciefp_list.append(Ciefp1)
		self.ciefp_list.append(Ciefp2A)
		self.ciefp_list.append(Ciefp2B)
		self.ciefp_list.append(Ciefp3A)
		self.ciefp_list.append(Ciefp3B)
		self.ciefp_list.append(Ciefp4A)
		self.ciefp_list.append(Ciefp4B)
		self.ciefp_list.append(Ciefp5)
		self.ciefp_list.append(Ciefp6)
		self.ciefp_list.append(Ciefp7)
		self.ciefp_list.append(Ciefp8)
		self.ciefp_list.append(Ciefp9)
		self.ciefp_list.append(Ciefp10)
		self.ciefp_list.append(Ciefp13)
		self.ciefp_list.append(Ciefp16)
		self.ciefp_list.append(Ciefp18)
		self.ciefp_list.append(CiefpM)
		self["menu"].moveToIndex(0)
		self["menu"].l.setList(self.ciefp_list)
		self.setTitle(_(App + " > Ciefp Settings"))
		os.system('wget ' + Ciefp + ' -O ' + Ciefp_zip)

	def menu_morpheus(self):
	    global menu
	    menu = 1
	    self.morph_list = []
	    self.morph_list.append(Morph1)
	    self.morph_list.append(Morph2)
	    self.morph_list.append(Morph3)
	    self.morph_list.append(Morph4)
	    self.morph_list.append(Morph5)
	    self.morph_list.append(Morph6)
	    self.morph_list.append(Morph7)
	    self.morph_list.append(Morph8)
	    self.morph_list.append(Morph9)
	    self.morph_list.append(Morph10)
	    self.morph_list.append(Morph11)
	    self.morph_list.append(Morph12)
	    self.morph_list.append(Morph13)
	    self.morph_list.append(Morph14)
	    self.morph_list.append(Morph15)
	    self.morph_list.append(Morph16)
	    self.morph_list.append(Morph17)
	    self.morph_list.append(Morph18)
	    self.morph_list.append(Morph19)
	    self.morph_list.append(Morph20)
	    self.morph_list.append(Morph21)
	    self.morph_list.append(Morph22)
	    self.morph_list.append(MorphM)
	    self["menu"].moveToIndex(0)
	    self["menu"].l.setList(self.morph_list)
	    self.setTitle(_(App + " > Morpheus883 Settings"))
	    os.system('wget ' + Morph + ' -O ' + Morph_zip)

	def check_github_api(self, api):
		global github_api
		req = compat_Request(api, headers={'User-Agent': 'Mozilla/5.0'})
		page = compat_urlopen(req).read()
		github_api = json.loads(page)
		return github_api

	def check_user_config(self):
		global user_config
		user_config_parser = configparser.ConfigParser()
		user_config_parser.read("/etc/enigma2/ONEupdaterE2/user_config.ini")
		user_config = user_config_parser['settings']
		return user_config

	def install_setting(self, name, fzip, folder):
		global installed
		installed = '0'
		try_author = name.split()[0]
		if try_author == "Ciefp":
			author = 'Ciefp'
		else:
			author = 'Morpheus883'
		today = datetime.today()
		install_date = today.strftime('%Y-%m-%d')
		os.system('mkdir -p ' + ONE_tmp)
		os.system("unzip " + fzip + " '" + folder + "/*' -d '" + ONE_tmp + "';")
		os.system('rm -rf /etc/enigma2/lamedb')
		os.system('rm -rf /etc/enigma2/*.radio')
		os.system('rm -rf /etc/enigma2/*.tv')
		os.system('mv -f ' + ONE_tmp + folder + '/* /etc/enigma2/;')
		eDVBDB.getInstance().reloadServicelist()
		eDVBDB.getInstance().reloadBouquets()
		os.system('rm -rf ' + ONE_tmp + ';')
		os.system('rm -rf /etc/enigma2/ONEupdaterE2/user_config.ini')
		os.system('echo "###################\n## ONEupdater E2 ##\n###################\n\n[settings]\nname = ' + name +'\ndate = ' + install_date + '\nauthor = ' + author +'\npath = ' + folder + '\n" > /etc/enigma2/ONEupdaterE2/user_config.ini')
		installed = '1'
		return True

	def loading(self):
	    self.session.open(MessageBox,("Loading"),  MessageBox.TYPE_INFO, timeout=4)

	def install_Picons(self, ulink):
	    today = datetime.today()
	    install_date = today.strftime('%Y-%m-%d')
	    os.system('rm -rf /etc/enigma2/ONEupdaterE2/user_picons.ini')
	    plink = subprocess.check_output(ulink, shell=True, universal_newlines=True)
	    os.system('echo "###################\n## ONEupdater E2 ##\n###################\n\n[settings]\ndate = ' + install_date + '\nlink = ' + plink + '\n" > /etc/enigma2/ONEupdaterE2/user_picons.ini')
	    os.system('mkdir -p ' + ONE_tmp)
	    os.system('wget ' + plink + ' -O ' + ONE_tmp + Picons_ipk)
	    os.system("opkg install " + ONE_tmp + Picons_ipk)
	    os.system('rm -rf ' + ONE_tmp + ';')
	    return True

	def installed(self, name):
	    self.session.open(MessageBox,(name + " Installed Successfully"),  MessageBox.TYPE_INFO, timeout=6)

	def update_settings(self, answer=False):
	    if answer:
	        try:
	            self.check_user_config()
	            date = user_config['date']
	            name = user_config['name']
	            author = user_config['author']
	            path = user_config['path']
	            api = ''
	            if author == "Ciefp":
	                api = Ciefp_api
	                fzip = Ciefp_zip
	                link = Ciefp
	            elif author == "Morpheus883":
	                api = Morph_api
	                fzip = Morph_zip
	                link = Morph
	            local_install_date = date
	            self.check_github_api(api)
	            remote_date = github_api['pushed_at']
	            strp_remote_date = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
	            remote_install_date = strp_remote_date.strftime('%Y-%m-%d')

	            if local_install_date < remote_install_date:
	                os.system('wget ' + link + ' -O ' + fzip)
	                self.install_setting(name, fzip, path)
	                if installed == '1':
	                    self.installed(name)
	        except:
	           trace_error
	           pass

	def ask_upgrade(self):
	  try:
	    self.check_user_config()
	    date = user_config['date']
	    name = user_config['name']
	    author = user_config['author']
	    local_install_date = date
	    if author == "Ciefp":
	      api = Ciefp_api
	    elif author == "Morpheus883":
	      api = Morph_api
	    self.check_github_api(api)
	    remote_date = github_api['pushed_at']
	    strp_remote_date = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
	    remote_install_date = strp_remote_date.strftime('%Y-%m-%d')

	    if local_install_date < remote_install_date:
	        self.session.openWithCallback(self.update_settings, MessageBox, _("%s released a new version of %s at %s \n\nDo you want to install it now?" % (author, name, remote_install_date)), MessageBox.TYPE_YESNO)
	  except:
	    trace_error()
	    pass


	def Exit(self):
		global menu
		if menu == 0:
			self.close()
		elif menu == 1:
			self["menu"].moveToIndex(0)
			self["menu"].l.setList(self.main_list)
			menu = 0
			self.setTitle(_(App))
		else:
			pass

	def ok(self):
			returnValue = self["menu"].l.getCurrentSelection()

			##Main Menu
			if returnValue == "Ciefp Settings":
				self.menu_ciefp()

			if returnValue == "Morpheus883 Settings":
				self.menu_morpheus()

			if returnValue == "Picons":
				self.menu_picons()

			##Ciefp Menu
			if returnValue == Ciefp1:
				if self.install_setting(Ciefp1, Ciefp_zip, Ciefp_folder + Ciefp1_path):
				    self.installed(Ciefp1)

			if returnValue == Ciefp2A:
				if self.install_setting(Ciefp2A, Ciefp_zip, Ciefp_folder + Ciefp2A_path):
				    self.installed(Ciefp2A)

			if returnValue == Ciefp2B:
				if self.install_setting(Ciefp2B, Ciefp_zip, Ciefp_folder + Ciefp2B_path):
				    self.installed(Ciefp2B)

			if returnValue == Ciefp3A:
				if self.install_setting(Ciefp3A, Ciefp_zip, Ciefp_folder + Ciefp3A_path):
				    self.installed(Ciefp3A)

			if returnValue == Ciefp3B:
				if self.install_setting(Ciefp3B, Ciefp_zip, Ciefp_folder + Ciefp3B_path):
				    self.installed(Ciefp3B)

			if returnValue == Ciefp4A:
				if self.install_setting(Ciefp4A, Ciefp_zip, Ciefp_folder + Ciefp4A_path):
				    self.installed(Ciefp4A)

			if returnValue == Ciefp4B:
				if self.install_setting(Ciefp4B, Ciefp_zip, Ciefp_folder + Ciefp4B_path):
				    self.installed(Ciefp4B)

			if returnValue == Ciefp5:
				if self.install_setting(Ciefp5, Ciefp_zip, Ciefp_folder + Ciefp5_path):
				    self.installed(Ciefp5)

			if returnValue == Ciefp6:
				if self.install_setting(Ciefp6, Ciefp_zip, Ciefp_folder + Ciefp6_path):
				    self.installed(Ciefp6)

			if returnValue == Ciefp7:
				if self.install_setting(Ciefp7, Ciefp_zip, Ciefp_folder + Ciefp7_path):
				    self.installed(Ciefp7)

			if returnValue == Ciefp8:
				if self.install_setting(Ciefp8, Ciefp_zip, Ciefp_folder + Ciefp8_path):
				    self.installed(Ciefp8)

			if returnValue == Ciefp9:
				if self.install_setting(Ciefp9, Ciefp_zip, Ciefp_folder + Ciefp9_path):
				    self.installed(Ciefp9)

			if returnValue == Ciefp10:
				if self.install_setting(Ciefp10, Ciefp_zip, Ciefp_folder + Ciefp10_path):
				    self.installed(Ciefp10)

			if returnValue == Ciefp13:
				if self.install_setting(Ciefp13, Ciefp_zip, Ciefp_folder + Ciefp13_path):
				    self.installed(Ciefp13)

			if returnValue == Ciefp16:
				if self.install_setting(Ciefp16, Ciefp_zip, Ciefp_folder + Ciefp16_path):
				    self.installed(Ciefp16)

			if returnValue == Ciefp18:
				if self.install_setting(Ciefp18, Ciefp_zip, Ciefp_folder + Ciefp18_path):
				    self.installed(Ciefp18)

			if returnValue == CiefpM:
				if self.install_setting(CiefpM, Ciefp_zip, Ciefp_folder + CiefpM_path):
				    self.installed(CiefpM)

			##Morpheus883 Menu
			if returnValue == Morph1:
			    if self.install_setting(Morph1, Morph_zip, Morph_folder + Morph1_path):
			        self.installed(Morph1)

			if returnValue == Morph2:
				if self.install_setting(Morph2, Morph_zip, Morph_folder + Morph2_path):
				    self.installed(Morph2)

			if returnValue == Morph3:
				if self.install_setting(Morph3, Morph_zip, Morph_folder + Morph3_path):
				    self.installed(Morph3)

			if returnValue == Morph4:
				if self.install_setting(Morph4, Morph_zip, Morph_folder + Morph4_path):
				    self.installed(Morph4)

			if returnValue == Morph5:
				if self.install_setting(Morph5, Morph_zip, Morph_folder + Morph5_path):
				    self.installed(Morph5)

			if returnValue == Morph6:
				if self.install_setting(Morph6, Morph_zip, Morph_folder + Morph6_path):
				    self.installed(Morph6)

			if returnValue == Morph7:
				if self.install_setting(Morph7, Morph_zip, Morph_folder + Morph7_path):
				    self.installed(Morph7)

			if returnValue == Morph8:
				if self.install_setting(Morph8, Morph_zip, Morph_folder + Morph8_path):
				    self.installed(Morph8)

			if returnValue == Morph9:
				if self.install_setting(Morph9, Morph_zip, Morph_folder + Morph9_path):
				    self.installed(Morph9)

			if returnValue == Morph10:
				if self.install_setting(Morph10, Morph_zip, Morph_folder + Morph10_path):
				    self.installed(Morph10)

			if returnValue == Morph11:
				if self.install_setting(Morph11, Morph_zip, Morph_folder + Morph11_path):
				    self.installed(Morph11)

			if returnValue == Morph12:
				if self.install_setting(Morph12, Morph_zip, Morph_folder + Morph12_path):
				    self.installed(Morph12)

			if returnValue == Morph13:
				if self.install_setting(Morph13, Morph_zip, Morph_folder + Morph13_path):
				    self.installed(Morph13)

			if returnValue == Morph14:
				if self.install_setting(Morph14, Morph_zip, Morph_folder + Morph14_path):
				    self.installed(Morph14)

			if returnValue == Morph15:
				if self.install_setting(Morph15, Morph_zip, Morph_folder + Morph15_path):
				    self.installed(Morph15)

			if returnValue == Morph16:
				if self.install_setting(Morph16, Morph_zip, Morph_folder + Morph16_path):
				    self.installed(Morph16)

			if returnValue == Morph17:
				if self.install_setting(Morph17, Morph_zip, Morph_folder + Morph17_path):
				    self.installed(Morph17)

			if returnValue == Morph18:
				if self.install_setting(Morph18, Morph_zip, Morph_folder + Morph18_path):
				    self.installed(Morph18)

			if returnValue == Morph19:
				if self.install_setting(Morph19, Morph_zip, Morph_folder + Morph19_path):
				    self.installed(Morph19)

			if returnValue == Morph20:
				if self.install_setting(Morph20, Morph_zip, Morph_folder + Morph20_path):
				    self.installed(Morph20)

			if returnValue == Morph21:
				if self.install_setting(Morph21, Morph_zip, Morph_folder + Morph21_path):
				    self.installed(Morph21)

			if returnValue == Morph22:
				if self.install_setting(Morph22, Morph_zip, Morph_folder + Morph22_path):
				    self.installed(Morph22)

			if returnValue == MorphM:
				if self.install_setting(MorphM, Morph_zip, Morph_folder + MorphM_path):
				    self.installed(MorphM)

			##Picons Menu
			if returnValue == Picons1:
			    if self.install_Picons(full_100_dr):
			        self.installed(Picons1)

			if returnValue == Picons14:
			    if self.install_Picons(full_100_dt):
			        self.installed(Picons14)

			if returnValue == Picons15:
			    if self.install_Picons(full_100_lt):
			        self.installed(Picons15)

			if returnValue == Picons16:
			    if self.install_Picons(full_220_dr):
			        self.installed(Picons16)

			if returnValue == Picons17:
			    if self.install_Picons(full_220_dt):
			        self.installed(Picons17)

			if returnValue == Picons18:
			    if self.install_Picons(full_220_lt):
			        self.installed(Picons18)

			if returnValue == Picons2:
			    if self.install_Picons(sat4_100_dr):
			        self.installed(Picons2)

			if returnValue == Picons3:
			    if self.install_Picons(sat4_100_dt):
			        self.installed(Picons3)

			if returnValue == Picons4:
			    if self.install_Picons(sat4_100_lt):
			        self.installed(Picons4)

			if returnValue == Picons5:
			    if self.install_Picons(ziggo_100_dr):
			        self.installed(Picons5)

			if returnValue == Picons6:
			    if self.install_Picons(ziggo_100_dt):
			        self.installed(Picons6)

			if returnValue == Picons7:
			    if self.install_Picons(ziggo_100_lt):
			        self.installed(Picons7)

			if returnValue == Picons8:
			    if self.install_Picons(sat4_220_dr):
			        self.installed(Picons8)

			if returnValue == Picons9:
			    if self.install_Picons(sat4_220_dt):
			        self.installed(Picons9)

			if returnValue == Picons10:
			    if self.install_Picons(sat4_220_lt):
			        self.installed(Picons10)

			if returnValue == Picons11:
			    if self.install_Picons(ziggo_220_dr):
			        self.installed(Picons11)

			if returnValue == Picons12:
			    if self.install_Picons(ziggo_220_dt):
			        self.installed(Picons12)

			if returnValue == Picons13:
			    if self.install_Picons(ziggo_220_lt):
			        self.installed(Picons13)

	def update_me(self):
		remote_version = '0.0'
		remote_changelog = ''
		req = compat_Request(ONE_installer, headers={'User-Agent': 'Mozilla/5.0'})
		page = compat_urlopen(req).read()
		if PY3:
			data = page.decode("utf-8")
		else:
			data = page.encode("utf-8")
		if data:
			lines = data.split("\n")
			for line in lines:
				if line.startswith("version"):
					remote_version = line.split("=")
					remote_version = line.split("'")[1]
				if line.startswith("changelog"):
					remote_changelog = line.split("=")
					remote_changelog = line.split("'")[1]
					break

		if float(Version) < float(remote_version):
			new_version = remote_version
			new_changelog = remote_changelog
			self.session.openWithCallback(self.install_update, MessageBox, _("New version %s is available.\n\nChangelog: %s \n\nDo you want to install it now?" % (new_version, new_changelog)), MessageBox.TYPE_YESNO)
		else:
		    self.ask_upgrade()

	def install_update(self, answer=False):
		if answer:
			self.session.open(Console, title='Upgrading...', cmdlist='wget -q "--no-check-certificate" https://git.multics.one/Qu4k3/ONEupdaterE2/raw/branch/main/installer.sh -O - | /bin/sh', finishedCallback=self.myCallback, closeOnSuccess=False)
		else:
		    self.ask_upgrade()

	def myCallback(self, result):
		return

	#def restartEnigma(self, answer=False):
		#if answer:
			#self.session.open(TryQuitMainloop, 3) # 0=Toggle StandBy ; 1=DeepStandBy ; 2=Reboot System ; 3=Restart Enigma ; 4=Wake Up ; 5=Enter Standbyp

##############################
##############################

####################################################
####################################################

def main(session):
	session.open(ONEupdater)

####################################################

def Plugins(**kwargs):
	return PluginDescriptor(name=App, description=App + ' v'+ Version, where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU], icon="one.jpg", fnc = main)

####################################################
