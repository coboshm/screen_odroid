#!/bin/bash

SOFTWARE_ODROID="http://192.168.1.33:3000/odroid/odroidSoftware.zip"
SOFTWARE_ODROID_BOTTLE="http://192.168.1.33:3000/odroid/odroidBottle.zip"
INITNAME="script_init"

echo "Installing...it might take a while (5/10 minutes)"
echo "Updating system package database..."
sudo apt-get -qq update > /dev/null

echo "Installing dependencies..."
sudo apt-get -y -qq install python-pip python-simplejson libopencv-dev python-opencv python-imaging python-dev python-numpy python-dev python-tk python-mechanize watchdog supervisor > /dev/null
sudo apt-get -y -qq install cron > /dev/null

rm -rf /tmp/log/impactScreen
mkdir /tmp/log/impactScreen
$(rm -rf $HOME/.impactScreen)
$(mkdir $HOME/.impactScreen)
$(rm -rf $HOME/.bottle_server)
$(mkdir $HOME/.bottle_server)



wget -nH --cut-dirs=2 --no-parent $SOFTWARE_ODROID > /dev/null 2> /dev/null
sleep 5
unzip odroidSoftware.zip -d .impactScreen > /dev/null 2> /dev/null
rm odroidSoftware.zip
rm -rf .impactScreen/__MACOSX/
chmod -R 777 .impactScreen/

wget -nH --cut-dirs=2 --no-parent $SOFTWARE_ODROID_BOTTLE > /dev/null 2> /dev/null
sleep 5
unzip odroidBottle.zip -d .bottle_server > /dev/null 2> /dev/null
rm odroidBottle.zip
rm -rf .bottle_server/__MACOSX/
chmod -R 777 .bottle_server/

echo "Installing more dependencies..."
sudo pip install -r .impactScreen/requirements.txt -q

echo "Adding ImpactScreen to X auto start..."
mkdir -p "$HOME/.config/lxsession/Lubuntu/"
echo "@$HOME/.impactScreen/installation/xloader.sh" > "$HOME/.config/lxsession/Lubuntu/autostart"

rm /etc/supervisor/conf.d/impactScreen.conf
sudo ln -s "$HOME/.impactScreen/installation/supervisor_impactScreen.conf" /etc/supervisor/conf.d/impactScreen.conf
sudo /etc/init.d/supervisor stop > /dev/null
sudo /etc/init.d/supervisor start > /dev/null


[ -f "$HOME/.config/openbox/lubuntu-rc.xml" ] && \
    mv "$HOME/.config/openbox/lubuntu-rc.xml" "$HOME/.config/openbox/lubuntu-rc.xml.bak"
[ -d "$HOME/.config/openbox" ] || mkdir -p "$HOME/.config/openbox"
rm "$HOME/.config/openbox/lubuntu-rc.xml"
ln -s "$HOME/.impactScreen/installation/lxde-rc.xml" "$HOME/.config/openbox/lubuntu-rc.xml"
[ -f "$HOME/.config/lxpanel/Lubuntu/panels/panel" ] && \
    mv "$HOME/.config/lxpanel/Lubuntu/panels/panel" "$HOME/.config/lxpanel/Lubuntu/panels/panel.bak"


# Cover both situations, as there have been traces of both in recent versions.
[ -f "/etc/xdg/lxsession/LXDE/autostart" ] && \
    sudo mv "/etc/xdg/lxsession/LXDE/autostart" "/etc/xdg/lxsession/LXDE/autostart.bak"
[ -f "/etc/xdg/lxsession/Lubuntu/autostart" ] && \
    sudo mv "/etc/xdg/lxsession/Lubuntu/autostart" "/etc/xdg/lxsession/Lubuntu/autostart.bak"
[ -f "/etc/xdg/lxsession/Lubuntu-Netbook/autostart" ] && \
    sudo mv "/etc/xdg/lxsession/Lubuntu-Netbook/autostart" "/etc/xdg/lxsession/Lubuntu-Netbook/autostart.bak"

echo "Restarting..."
sudo shutdown -r now
