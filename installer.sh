#!/bin/bash
##setup command=wget -q "--no-check-certificate" https://git.multics.one/Qu4k3/ONEupdaterE2/raw/branch/main/installer.sh -O - | /bin/sh

######### Only This 2 lines to edit with new version ######
version='2.8'
changelog='\nFixed bug on AutoUpdater'
##############################################################

TMPPATH=/tmp/ONEupdaterE2

if [ ! -d /usr/lib64 ]; then
	PLUGINPATH=/usr/lib/enigma2/python/Plugins/Extensions/ONEupdater
else
	PLUGINPATH=/usr/lib64/enigma2/python/Plugins/Extensions/ONEupdater
fi

# check depends packges
if [ -f /var/lib/dpkg/status ]; then
   STATUS=/var/lib/dpkg/status
   OSTYPE=DreamOs
else
   STATUS=/var/lib/opkg/status
   OSTYPE=Dream
fi
echo ""
if python --version 2>&1 | grep -q '^Python 3\.'; then
	echo "You have Python3 image"
	PYTHON=PY3
	Packagesix=python3-six
	Packagerequests=python3-requests
else
	echo "You have Python2 image"
	PYTHON=PY2
	Packagerequests=python-requests
fi

if [ $PYTHON = "PY3" ]; then
	if grep -qs "Package: $Packagesix" cat $STATUS ; then
		echo ""
	else
		opkg update && opkg install python3-six
	fi
fi
echo ""
if grep -qs "Package: $Packagerequests" cat $STATUS ; then
	echo ""
else
	echo "Need to install $Packagerequests"
	echo ""
	if [ $OSTYPE = "DreamOs" ]; then
		apt-get update && apt-get install python-requests -y
	elif [ $PYTHON = "PY3" ]; then
		opkg update && opkg install python3-requests
	elif [ $PYTHON = "PY2" ]; then
		opkg update && opkg install python-requests
	fi
fi
echo ""

## Remove tmp directory
[ -r $TMPPATH ] && rm -f $TMPPATH > /dev/null 2>&1

## Remove old plugin directory
[ -r $PLUGINPATH ] && rm -rf $PLUGINPATH

# Download and install plugin
# check depends packges
mkdir -p $TMPPATH
cd $TMPPATH
set -e
if [ -f /var/lib/dpkg/status ]; then
   echo "# Your image is OE2.5/2.6 #"
   echo ""
   echo ""
else
   echo "# Your image is OE2.0 #"
   echo ""
   echo ""
fi
   wget https://git.multics.one/Qu4k3/ONEupdaterE2/archive/main.tar.gz
   tar -xzf main.tar.gz
   cp -r 'oneupdatere2/usr' '/'
if [ ! -f /etc/enigma2/ONEupdaterE2/user-config.ini ]; then
	mkdir -p /etc/enigma2/ONEupdaterE2
	cp -r ${PLUGINPATH}/user/user-config.ini /etc/enigma2/ONEupdaterE2/user-config.ini
fi
set +e
cd
sleep 2

### Check if plugin installed correctly
if [ ! -d $PLUGINPATH ]; then
	echo "Some thing wrong .. Plugin not installed"
	exit 1
fi

rm -rf $TMPPATH > /dev/null 2>&1
sync
echo ""
echo ""
echo "#########################################################"
echo "#          ONEupdaterE2 INSTALLED SUCCESSFULLY          #"
echo "#                 developed by Qu4k3                    #"
echo "#                                                       #"
echo "#                  https://multics.ONE                  #"
echo "#########################################################"
echo "#           your Device will RESTART Now                #"
echo "#########################################################"
sleep 5
killall -9 enigma2
exit 0
