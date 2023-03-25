###################
## ONEupdater E2 ##
###################

from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from Components.MenuList import MenuList
from Components.Label import Label
from enigma import *
import os

App = 'ONEupdater E2'
Version = '1.0'
Developer = 'Qu4k3'
ONE = 'http://multics.ONE'
Ciefp = 'https://github.com/ciefp/ciefpsettings-enigma2/archive/refs/heads/master.zip'
Ciefp1 = 'Ciefp Settings 1 SAT (19E)'
Ciefp2 = 'Ciefp Settings 2 SAT (19E 16E)'
Ciefp3 = 'Ciefp Settings 3 SAT (19E 16E 13E)'
Ciefp4 = 'Ciefp Settings 4 SAT (19E 16E 13E 0.8W)'
Ciefp5 = 'Ciefp Settings 5 SAT (19E 16E 13E 1.9E 0.8W)'
Ciefp6 = 'Ciefp Settings 6 SAT (23E 19E 16E 13E 1.9E 0.8W)'
Ciefp7 = 'Ciefp Settings 7 SAT (23E 19E 16E 13E 4.8E 1.9E 0.8W)'
Ciefp8 = 'Ciefp Settings 8 SAT (28E 23E 19E 16E 13E 4.8E 1.9E 0.8W)'
Ciefp9 = 'Ciefp Settings 9 SAT (39E 28E 23E 19E 16E 13E 4.8E 1.9E 0.8W)'
CiefpM = 'Ciefp Settings Motor (68E - 30W)'
		
def main(session):
	session.open(ONEupdater)

def Plugins(**kwargs):
	return PluginDescriptor(name=App, description=App + ' v'+ Version, where = PluginDescriptor.WHERE_PLUGINMENU, icon="one.jpg", fnc = main)

class ONEupdater(Screen):
	skin = """
        <screen title="ONEupdater E2" position="center,center" size="710,500">
            <widget name="menu" position="25,70" size="660,315" itemHeight="45" scrollbarMode="showOnDemand" />
            <widget name="Developer" position="25,420" size="660,60" font="Regular;22" halign="center" valign="center" />
            <widget name="Website" position="440,5" size="200,25" font="Regular;22" halign="center" valign="center" />
        </screen>
        """
		
	def __init__(self, session, args = None):
		self.skin = ONEupdater.skin
		self.session = session
		Screen.__init__(self, session)
			
		ciefp_list = []
		ciefp_list.append(Ciefp1)
		ciefp_list.append(Ciefp2)
		ciefp_list.append(Ciefp3)
		ciefp_list.append(Ciefp4)
		ciefp_list.append(Ciefp5)
		ciefp_list.append(Ciefp6)
		ciefp_list.append(Ciefp7)
		ciefp_list.append(Ciefp8)
		ciefp_list.append(Ciefp9)
		ciefp_list.append(CiefpM)
		self["menu"] = MenuList(ciefp_list)
		self["Developer"] = Label("Developed by " + Developer)
		self["Website"] = Label(ONE)
			
		self["actions"] = ActionMap(["OkCancelActions"],{"ok": self.menu_ciefp, "cancel": self.close}, -1)

	def menu_ciefp(self):
		returnValue = self["menu"].l.getCurrentSelection()
		if returnValue is not None:
			
			os.system('wget ' + Ciefp + ' -O /tmp/ONEupdater_ciefp_settings.zip')
			
			if returnValue == Ciefp1:
				os.system("unzip /tmp/ONEupdater_ciefp_settings.zip 'ciefpsettings-enigma2-master/ciefp-E2-1sat-19E/*' -d '/tmp/ONEupdater/';")
				os.system('rm -rf /etc/enigma2/lamedb')
				os.system('rm -rf /etc/enigma2/*.radio')
				os.system('rm -rf /etc/enigma2/*.tv')
				os.system("mv -f /tmp/ONEupdater/ciefpsettings-enigma2-master/ciefp-E2-1sat-19E/* /etc/enigma2/;")
				eDVBDB.getInstance().reloadServicelist()
				eDVBDB.getInstance().reloadBouquets()
				os.system("rm -rf /tmp/ONEupdater/;")
				self.session.open(MessageBox,(Ciefp1 + " Installed Successfully"),  MessageBox.TYPE_INFO, timeout=6)
				self.close()

			if returnValue == Ciefp2:
				os.system("unzip /tmp/ONEupdater_ciefp_settings.zip 'ciefpsettings-enigma2-master/ciefp-E2-2sat-19E-16E/*' -d '/tmp/ONEupdater/';")
				os.system('rm -rf /etc/enigma2/lamedb')
				os.system('rm -rf /etc/enigma2/*.radio')
				os.system('rm -rf /etc/enigma2/*.tv')
				os.system("mv -f /tmp/ONEupdater/ciefpsettings-enigma2-master/ciefp-E2-2sat-19E-16E/* /etc/enigma2/;")
				eDVBDB.getInstance().reloadServicelist()
				eDVBDB.getInstance().reloadBouquets()
				os.system("rm -rf /tmp/ONEupdater/;")
				self.session.open(MessageBox,(Ciefp2 + " Installed Successfully"),  MessageBox.TYPE_INFO, timeout=6)
				self.close()

			if returnValue == Ciefp3:
				os.system("unzip /tmp/ONEupdater_ciefp_settings.zip 'ciefpsettings-enigma2-master/ciefp-E2-3sat-19E-16E-13E/*' -d '/tmp/ONEupdater/';")
				os.system('rm -rf /etc/enigma2/lamedb')
				os.system('rm -rf /etc/enigma2/*.radio')
				os.system('rm -rf /etc/enigma2/*.tv')
				os.system("mv -f /tmp/ONEupdater/ciefpsettings-enigma2-master/ciefp-E2-3sat-19E-16E-13E/* /etc/enigma2/;")
				eDVBDB.getInstance().reloadServicelist()
				eDVBDB.getInstance().reloadBouquets()
				os.system("rm -rf /tmp/ONEupdater/;")
				self.session.open(MessageBox,(Ciefp3 + " Installed Successfully"),  MessageBox.TYPE_INFO, timeout=6)
				self.close()
				
			if returnValue == Ciefp4:
				os.system("unzip /tmp/ONEupdater_ciefp_settings.zip 'ciefpsettings-enigma2-master/ciefp-E2-4sat-19E-16E-13E-0.8W/*' -d '/tmp/ONEupdater/';")
				os.system('rm -rf /etc/enigma2/lamedb')
				os.system('rm -rf /etc/enigma2/*.radio')
				os.system('rm -rf /etc/enigma2/*.tv')
				os.system("mv -f /tmp/ONEupdater/ciefpsettings-enigma2-master/ciefp-E2-4sat-19E-16E-13E-0.8W/* /etc/enigma2/;")
				eDVBDB.getInstance().reloadServicelist()
				eDVBDB.getInstance().reloadBouquets()
				os.system("rm -rf /tmp/ONEupdater/;")
				self.session.open(MessageBox,(Ciefp4 + " Installed Successfully"),  MessageBox.TYPE_INFO, timeout=6)
				self.close()

			if returnValue == Ciefp5:
				os.system("unzip /tmp/ONEupdater_ciefp_settings.zip 'ciefpsettings-enigma2-master/ciefp-E2-5sat-19E-16E-13E-1.9E-0.8W/*' -d '/tmp/ONEupdater/';")
				os.system('rm -rf /etc/enigma2/lamedb')
				os.system('rm -rf /etc/enigma2/*.radio')
				os.system('rm -rf /etc/enigma2/*.tv')
				os.system("mv -f /tmp/ONEupdater/ciefpsettings-enigma2-master/ciefp-E2-5sat-19E-16E-13E-1.9E-0.8W/* /etc/enigma2/;")
				eDVBDB.getInstance().reloadServicelist()
				eDVBDB.getInstance().reloadBouquets()
				os.system("rm -rf /tmp/ONEupdater/;")
				self.session.open(MessageBox,(Ciefp5 + " Installed Successfully"),  MessageBox.TYPE_INFO, timeout=6)
				self.close()

			if returnValue == Ciefp6:
				os.system("unzip /tmp/ONEupdater_ciefp_settings.zip 'ciefpsettings-enigma2-master/ciefp-E2-6sat-23E-19E-16E-13E-1.9E-0.8W/*' -d '/tmp/ONEupdater/';")
				os.system('rm -rf /etc/enigma2/lamedb')
				os.system('rm -rf /etc/enigma2/*.radio')
				os.system('rm -rf /etc/enigma2/*.tv')
				os.system("mv -f /tmp/ONEupdater/ciefpsettings-enigma2-master/ciefp-E2-6sat-23E-19E-16E-13E-1.9E-0.8W/* /etc/enigma2/;")
				eDVBDB.getInstance().reloadServicelist()
				eDVBDB.getInstance().reloadBouquets()
				os.system("rm -rf /tmp/ONEupdater/;")
				self.session.open(MessageBox,(Ciefp6 + " Installed Successfully"),  MessageBox.TYPE_INFO, timeout=6)
				self.close()

			if returnValue == Ciefp7:
				os.system("unzip /tmp/ONEupdater_ciefp_settings.zip 'ciefpsettings-enigma2-master/ciefp-E2-7sat-23E-19E-16E-13E-4.8E-1.9E-0.8W/*' -d '/tmp/ONEupdater/';")
				os.system('rm -rf /etc/enigma2/lamedb')
				os.system('rm -rf /etc/enigma2/*.radio')
				os.system('rm -rf /etc/enigma2/*.tv')
				os.system("mv -f /tmp/ONEupdater/ciefpsettings-enigma2-master/ciefp-E2-7sat-23E-19E-16E-13E-4.8E-1.9E-0.8W/* /etc/enigma2/;")
				eDVBDB.getInstance().reloadServicelist()
				eDVBDB.getInstance().reloadBouquets()
				os.system("rm -rf /tmp/ONEupdater/;")
				self.session.open(MessageBox,(Ciefp7 + " Installed Successfully"),  MessageBox.TYPE_INFO, timeout=6)
				self.close()
				
			if returnValue == Ciefp8:
				os.system("unzip /tmp/ONEupdater_ciefp_settings.zip 'ciefpsettings-enigma2-master/ciefp-E2-8sat-28E-23E-19E-16E-13E-4.8E-1.9E-0.8W/*' -d '/tmp/ONEupdater/';")
				os.system('rm -rf /etc/enigma2/lamedb')
				os.system('rm -rf /etc/enigma2/*.radio')
				os.system('rm -rf /etc/enigma2/*.tv')
				os.system("mv -f /tmp/ONEupdater/ciefpsettings-enigma2-master/ciefp-E2-8sat-28E-23E-19E-16E-13E-4.8E-1.9E-0.8W/* /etc/enigma2/;")
				eDVBDB.getInstance().reloadServicelist()
				eDVBDB.getInstance().reloadBouquets()
				os.system("rm -rf /tmp/ONEupdater/;")
				self.session.open(MessageBox,(Ciefp8 + " Installed Successfully"),  MessageBox.TYPE_INFO, timeout=6)
				self.close()

			if returnValue == Ciefp9:
				os.system("unzip /tmp/ONEupdater_ciefp_settings.zip 'ciefpsettings-enigma2-master/ciefp-E2-9sat-39E-28E-23E-19E-16E-13E-4.8E-1.9E-0.8W/*' -d '/tmp/ONEupdater/';")
				os.system('rm -rf /etc/enigma2/lamedb')
				os.system('rm -rf /etc/enigma2/*.radio')
				os.system('rm -rf /etc/enigma2/*.tv')
				os.system("mv -f /tmp/ONEupdater/ciefpsettings-enigma2-master/ciefp-E2-9sat-39E-28E-23E-19E-16E-13E-4.8E-1.9E-0.8W/* /etc/enigma2/;")
				eDVBDB.getInstance().reloadServicelist()
				eDVBDB.getInstance().reloadBouquets()
				os.system("rm -rf /tmp/ONEupdater/;")
				self.session.open(MessageBox,(Ciefp9 + " Installed Successfully"),  MessageBox.TYPE_INFO, timeout=6)
				self.close()

			if returnValue == CiefpM:
				os.system("unzip /tmp/ONEupdater_ciefp_settings.zip 'ciefpsettings-enigma2-master/ciefp-E2-motor-68E-30W-VOD/*' -d '/tmp/ONEupdater/';")
				os.system('rm -rf /etc/enigma2/lamedb')
				os.system('rm -rf /etc/enigma2/*.radio')
				os.system('rm -rf /etc/enigma2/*.tv')
				os.system("mv -f /tmp/ONEupdater/ciefpsettings-enigma2-master/ciefp-E2-motor-68E-30W-VOD/* /etc/enigma2/;")
				eDVBDB.getInstance().reloadServicelist()
				eDVBDB.getInstance().reloadBouquets()
				os.system("rm -rf /tmp/ONEupdater/;")
				self.session.open(MessageBox,(CiefpM + " Installed Successfully"),  MessageBox.TYPE_INFO, timeout=6)
				self.close()
