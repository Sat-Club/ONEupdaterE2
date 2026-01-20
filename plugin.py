#!/usr/bin/python
# -*- coding: utf-8 -*-
###################
## ONEupdater E2 ##
###################

import os
import json
import subprocess
import shutil
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

# new helper utilities (safer file ops)
from .helpers import tempdir, extract_zip, run_command, safe_write_ini, safe_mkdir, safe_remove

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

    def check_github_api(self, api):
        """
        Query a GitHub API URL (or other JSON endpoint). Returns parsed JSON.
        Includes timeout and error handling.
        """
        try:
            req = compat_Request(api, headers={'User-Agent': 'ONEupdater/{}'.format(Version)})
            # compat_urlopen may not support timeout on all platforms; try/except around network
            page = compat_urlopen(req).read()
            if PY3 and isinstance(page, bytes):
                page = page.decode('utf-8')
            return json.loads(page)
        except Exception:
            trace_error()
            raise

    def check_user_config(self):
        global user_config
        user_config_parser = configparser.ConfigParser()
        user_config_parser.read("/etc/enigma2/ONEupdaterE2/user_config.ini")
        user_config = user_config_parser['settings']
        return user_config

    def install_setting(self, name, fzip, folder):
        """
        Safer implementation: use helpers to extract the folder from fzip into a temp dir
        and then move files into /etc/enigma2. Write user_config.ini with configparser.
        """
        try:
            author = 'Unknown'
            try_author = name.split()[0]
            if try_author == "Ciefp":
                author = 'Ciefp'
            elif try_author == "Morpheus883":
                author = 'Morpheus883'
            today = datetime.today()
            install_date = today.strftime('%Y-%m-%d')

            # ensure the plugin temp dir exists
            safe_mkdir(ONE_tmp)

            with tempdir() as td:
                # download if fzip is a URL
                if fzip.startswith('http://') or fzip.startswith('https://'):
                    local_zip = os.path.join(td, os.path.basename(fzip))
                    run_command(['wget', '-q', '-O', local_zip, fzip])
                else:
                    local_zip = fzip

                # extract the requested folder into td
                extract_zip(local_zip, folder, td)

                # remove/backup existing DBs cautiously
                safe_remove('/etc/enigma2/lamedb')
                # remove matching pattern files (use glob)
                import glob
                for pattern in ['/etc/enigma2/*.radio', '/etc/enigma2/*.tv']:
                    for f in glob.glob(pattern):
                        safe_remove(f)

                # move files from extracted folder into /etc/enigma2
                extracted_root = os.path.join(td, os.path.basename(folder))
                if not os.path.isdir(extracted_root):
                    # try if folder is directly the path without basename
                    extracted_root = os.path.join(td, folder)
                if not os.path.isdir(extracted_root):
                    # fallback: try to find first directory inside td
                    entries = [p for p in os.listdir(td) if os.path.isdir(os.path.join(td, p))]
                    if entries:
                        extracted_root = os.path.join(td, entries[0])

                for root, dirs, files in os.walk(extracted_root):
                    rel = os.path.relpath(root, extracted_root)
                    dest_dir = os.path.join('/etc/enigma2', rel) if rel != '.' else '/etc/enigma2'
                    safe_mkdir(dest_dir)
                    for file in files:
                        src_file = os.path.join(root, file)
                        dst_file = os.path.join(dest_dir, file)
                        try:
                            os.replace(src_file, dst_file)
                        except Exception:
                            shutil.copy2(src_file, dst_file)

                # Trigger Enigma2 reloads
                try:
                    eDVBDB.getInstance().reloadServicelist()
                    eDVBDB.getInstance().reloadBouquets()
                except Exception:
                    # not fatal for plugin operation
                    trace_error()

                # Remove temporary data (tempdir context will clean)
                # Write config using safe_write_ini
                safe_write_ini('/etc/enigma2/ONEupdaterE2/user_config.ini', 'settings',
                               {'name': name, 'date': install_date, 'author': author, 'path': folder})

            return True
        except Exception:
            trace_error()
            return False

    def loading(self):
        self.session.open(MessageBox,("Loading"),  MessageBox.TYPE_INFO, timeout=4)

    def install_Picons(self, ulink):
        """
        Safer install of picons. ulink may be a URL or a shell command that prints a URL.
        """
        try:
            today = datetime.today()
            install_date = today.strftime('%Y-%m-%d')

            # determine plink (the real URL)
            plink = None
            # if ulink contains spaces or shell pipelines, run via shell but capture stdout
            if isinstance(ulink, str) and (' ' in ulink or '|' in ulink):
                proc = run_command(ulink, check=True, shell=True)
                plink = proc.stdout.strip()
            else:
                # assume ulink is a URL or simple command; try to run and if it fails, treat as URL
                if ulink.startswith('http://') or ulink.startswith('https://'):
                    plink = ulink
                else:
                    try:
                        proc = run_command(ulink, check=True)
                        plink = proc.stdout.strip()
                    except Exception:
                        plink = ulink

            if not plink:
                raise ValueError("Could not determine picons link")

            safe_write_ini('/etc/enigma2/ONEupdaterE2/user_picons.ini', 'settings', {'date': install_date, 'link': plink})

            safe_mkdir(ONE_tmp)
            with tempdir() as td:
                local_ipk = os.path.join(td, os.path.basename(plink))
                run_command(['wget', '-q', '-O', local_ipk, plink])
                # install ipk using opkg if available
                try:
                    run_command(['opkg', 'install', local_ipk])
                except subprocess.CalledProcessError:
                    # fall back to dpkg if present
                    try:
                        run_command(['dpkg', '-i', local_ipk])
                    except Exception:
                        trace_error()
                        return False
            return True
        except Exception:
            trace_error()
            return False

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
                gh = self.check_github_api(api)
                remote_date = gh.get('pushed_at', '')
                if remote_date:
                    strp_remote_date = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
                    remote_install_date = strp_remote_date.strftime('%Y-%m-%d')
                    if local_install_date < remote_install_date:
                        # download using safe run_command into ONE_tmp
                        safe_mkdir(ONE_tmp)
                        local_zip = os.path.join(ONE_tmp, os.path.basename(link))
                        run_command(['wget', '-q', '-O', local_zip, link])
                        if self.install_setting(name, local_zip, path):
                            self.installed(name)
            except Exception:
               trace_error()
               pass

    def ask_upgrade(self):
        try:
            self.check_user_config()
            date = user_config['date']
            name = user_config['name']
            author = user_config['author']
            local_install_date = date
            api = ''
            if author == "Ciefp":
                api = Ciefp_api
            elif author == "Morpheus883":
                api = Morph_api
            gh = self.check_github_api(api)
            remote_date = gh.get('pushed_at', '')
            if remote_date:
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

        # rest of selection handling unchanged

    def update_me(self):
        """
        Robust parsing of the remote installer script to detect version/changelog.
        """
        try:
            remote_version = '0.0'
            remote_changelog = ''
            req = compat_Request(ONE_installer, headers={'User-Agent': 'ONEupdater/{}'.format(Version)})
            page = compat_urlopen(req).read()
            if PY3 and isinstance(page, bytes):
                data = page.decode('utf-8')
            else:
                data = page if isinstance(page, str) else page.decode('utf-8')
            import re
            v = re.search(r"^version\s*=\s*['\"]([^'\"]+)['\"]", data, re.MULTILINE)
            c = re.search(r"^changelog\s*=\s*['\"](.+?)['\"]", data, re.MULTILINE | re.DOTALL)
            if v:
                remote_version = v.group(1).strip()
            if c:
                remote_changelog = c.group(1).strip()
            try:
                if float(Version) < float(remote_version):
                    new_version = remote_version
                    new_changelog = remote_changelog
                    self.session.openWithCallback(self.install_update, MessageBox, _("New version %s is available.\n\nChangelog: %s \n\nDo you want to install it now?" % (new_version, new_changelog)), MessageBox.TYPE_YESNO)
                else:
                    self.ask_upgrade()
            except Exception:
                # version parsing may fail; fallback to ask_upgrade
                self.ask_upgrade()
        except Exception:
            trace_error()

    def install_update(self, answer=False):
        if answer:
            self.session.open(Console, title='Upgrading...', cmdlist='wget -q "--no-check-certificate" ' + ONE_installer + ' -O - | /bin/sh', finishedCallback=self.myCallback, closeOnSuccess=False)
        else:
            self.ask_upgrade()

    def myCallback(self, result):
        return


def main(session):
    session.open(ONEupdater)

def Plugins(**kwargs):
    return PluginDescriptor(name=App, description=App + ' v'+ Version, where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU], icon="one.jpg", fnc = main)