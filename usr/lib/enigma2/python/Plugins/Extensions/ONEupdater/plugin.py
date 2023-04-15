###################
## ONEupdater E2 ##
###################

from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap, NumberActionMap
from Plugins.Plugin import PluginDescriptor
from Components.MenuList import MenuList
from Components.Label import Label
from enigma import *
import os
from .extras.compat import compat_urlopen, compat_Request
from .extras.Console import Console
from threading import Timer
from .Ciefp import *
from .Morpheus883 import *

App = 'ONEupdater E2'
Version = '2.1'
Developer = 'Qu4k3'
ONE = 'https://multics.ONE'
ONE_tmp =  '/tmp/ONEupdater/'
ONE_installer = 'https://git.multics.one/Qu4k3/ONEupdaterE2/raw/branch/main/installer.sh'


class ONEupdater(Screen):
	skin = """
        <screen title="ONEupdater E2" position="center,center" size="900,500">
            <widget name="menu" position="25,30" size="800,400" itemHeight="45" scrollbarMode="showOnDemand" />
            <widget name="version" position="left,475" size="100,20" font="Regular;18" halign="center" valign="center" />
            <widget name="Developer" position="center,475" size="300,22" font="Regular;20" halign="center" valign="center" />
            <widget name="Website" position="623,475" size="400,20" font="Regular;18" halign="center" valign="center" />
        </screen>
        """
		
	def __init__(self, session, args = None):
		self.skin = ONEupdater.skin
		self.session = session
		Screen.__init__(self, session)
		self.main_menu()
		
	def main_menu(self):
		global menu
		self.main_list = []
		self.main_list.append("Ciefp Settings")
		self.main_list.append("Morpheus883 Settings")
		self["menu"] = MenuList(self.main_list)
		self["Developer"] = Label("Developed by " + Developer)
		self["Website"] = Label(ONE)
		self["version"] = Label("Version " + Version)
		self["actions"] = ActionMap(["OkCancelActions", "NumberActions"],{"ok": self.ok, "cancel": self.Exit}, -1)
		menu = 0
		t = Timer(2.0, self.update_me)
		t.start()
	
	def menu_ciefp(self):
		global menu
		menu = 1
		self.ciefp_list = []
		self.ciefp_list.append(Ciefp1)
		self.ciefp_list.append(Ciefp2)
		self.ciefp_list.append(Ciefp3)
		self.ciefp_list.append(Ciefp4)
		self.ciefp_list.append(Ciefp5)
		self.ciefp_list.append(Ciefp6)
		self.ciefp_list.append(Ciefp7)
		self.ciefp_list.append(Ciefp8)
		self.ciefp_list.append(Ciefp9)
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
	    
	def install_setting(self, name, zip, folder):
		os.system("unzip " + zip + " '" + folder + "/*' -d '" + ONE_tmp + "';")
		os.system('rm -rf /etc/enigma2/lamedb')
		os.system('rm -rf /etc/enigma2/*.radio')
		os.system('rm -rf /etc/enigma2/*.tv')
		os.system('mv -f ' + ONE_tmp + folder + '/* /etc/enigma2/;')
		eDVBDB.getInstance().reloadServicelist()
		eDVBDB.getInstance().reloadBouquets()
		os.system('rm -rf ' + ONE_tmp + ';')
		self.session.open(MessageBox,(name + " Installed Successfully"),  MessageBox.TYPE_INFO, timeout=6)
		return


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
			
			##Ciefp Menu
			if returnValue == Ciefp1:
				self.install_setting(Ciefp1, Ciefp_zip, Ciefp_folder + Ciefp1_path)

			if returnValue == Ciefp2:
				self.install_setting(Ciefp2, Ciefp_zip, Ciefp_folder + Ciefp2_path)

			if returnValue == Ciefp3:
				self.install_setting(Ciefp3, Ciefp_zip, Ciefp_folder + Ciefp3_path)
				
			if returnValue == Ciefp4:
				self.install_setting(Ciefp4, Ciefp_zip, Ciefp_folder + Ciefp4_path)

			if returnValue == Ciefp5:
				self.install_setting(Ciefp5, Ciefp_zip, Ciefp_folder + Ciefp5_path)

			if returnValue == Ciefp6:
				self.install_setting(Ciefp6, Ciefp_zip, Ciefp_folder + Ciefp6_path)

			if returnValue == Ciefp7:
				self.install_setting(Ciefp7, Ciefp_zip, Ciefp_folder + Ciefp7_path)
				
			if returnValue == Ciefp8:
				self.install_setting(Ciefp8, Ciefp_zip, Ciefp_folder + Ciefp8_path)

			if returnValue == Ciefp9:
				self.install_setting(Ciefp9, Ciefp_zip, Ciefp_folder + Ciefp9_path)

			if returnValue == CiefpM:
				self.install_setting(CiefpM, Ciefp_zip, Ciefp_folder + CiefpM_path)
				
			##Morpheus883 Menu
			if returnValue == Morph1:
				self.install_setting(Morph1, Morph_zip, Morph_folder + Morph1_path)
				
			if returnValue == Morph2:
				self.install_setting(Morph2, Morph_zip, Morph_folder + Morph2_path)
				
			if returnValue == Morph3:
				self.install_setting(Morph3, Morph_zip, Morph_folder + Morph3_path)
				
			if returnValue == Morph4:
				self.install_setting(Morph4, Morph_zip, Morph_folder + Morph4_path)

			if returnValue == Morph5:
				self.install_setting(Morph5, Morph_zip, Morph_folder + Morph5_path)
				
			if returnValue == Morph6:
				self.install_setting(Morph6, Morph_zip, Morph_folder + Morph6_path)
				
			if returnValue == Morph7:
				self.install_setting(Morph7, Morph_zip, Morph_folder + Morph7_path)
				
			if returnValue == Morph7:
				self.install_setting(Morph8, Morph_zip, Morph_folder + Morph8_path)

			if returnValue == Morph9:
				self.install_setting(Morph9, Morph_zip, Morph_folder + Morph9_path)
				
			if returnValue == Morph10:
				self.install_setting(Morph10, Morph_zip, Morph_folder + Morph10_path)
				
			if returnValue == Morph11:
				self.install_setting(Morph11, Morph_zip, Morph_folder + Morph11_path)
				
			if returnValue == Morph12:
				self.install_setting(Morph12, Morph_zip, Morph_folder + Morph12_path)

			if returnValue == Morph13:
				self.install_setting(Morph13, Morph_zip, Morph_folder + Morph13_path)
				
			if returnValue == Morph14:
				self.install_setting(Morph14, Morph_zip, Morph_folder + Morph14_path)
				
			if returnValue == Morph15:
				self.install_setting(Morph15, Morph_zip, Morph_folder + Morph15_path)
				
			if returnValue == Morph16:
				self.install_setting(Morph16, Morph_zip, Morph_folder + Morph16_path)

			if returnValue == Morph17:
				self.install_setting(Morph17, Morph_zip, Morph_folder + Morph17_path)
				
			if returnValue == Morph18:
				self.install_setting(Morph18, Morph_zip, Morph_folder + Morph18_path)
				
			if returnValue == Morph19:
				self.install_setting(Morph19, Morph_zip, Morph_folder + Morph19_path)
				
			if returnValue == Morph20:
				self.install_setting(Morph20, Morph_zip, Morph_folder + Morph20_path)

			if returnValue == Morph21:
				self.install_setting(Morph21, Morph_zip, Morph_folder + Morph21_path)
				
			if returnValue == Morph22:
				self.install_setting(Morph22, Morph_zip, Morph_folder + Morph22_path)
				
			if returnValue == MorphM:
				self.install_setting(MorphM, Morph_zip, Morph_folder + MorphM_path)
				
	def update_me(self):
		remote_version = '0.0'
		req = compat_Request(ONE_installer, headers={'User-Agent': 'Mozilla/5.0'})
		page = compat_urlopen(req).read()
		data = page.decode("utf-8")
		if data:
			lines = data.split("\n")
			for line in lines:
				if line.startswith("version"):
					remote_version = line.split("=")
					remote_version = line.split("'")[1]
					break
		
		if float(Version) != float(remote_version) or float(Version) < float(remote_version):
			new_version = remote_version
			self.session.openWithCallback(self.install_update, MessageBox, _("New version %s is available.\n\nDo you want to install it now?" % (new_version)), MessageBox.TYPE_YESNO)

	def install_update(self, answer=False):
		if answer:
			self.session.open(Console, title='Upgrading...', cmdlist='wget -q "--no-check-certificate" https://git.multics.one/Qu4k3/ONEupdaterE2/raw/branch/main/installer.sh -O - | /bin/sh', finishedCallback=self.myCallback, closeOnSuccess=False)

	def myCallback(self, result):
		return

	#def restartEnigma(self, answer=False):
		#if answer:
			#self.session.open(TryQuitMainloop, 3) # 0=Toggle StandBy ; 1=DeepStandBy ; 2=Reboot System ; 3=Restart Enigma ; 4=Wake Up ; 5=Enter Standby

####################################################

def main(session):
	session.open(ONEupdater)

def Plugins(**kwargs):
	return PluginDescriptor(name=App, description=App + ' v'+ Version, where = PluginDescriptor.WHERE_PLUGINMENU, icon="one.jpg", fnc = main)


