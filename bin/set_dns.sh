#!/bin/bash
#
# This script upates the DNS server in /etc/resolv.conf
#
#       This script is expected to be called from a crontab entry like this:
#       */5 * * * *     /storage/.kodi/addons/plugin.program.plexusscraper/bin/set_dns.sh
#       Basic steps to update crontab:
#       o VISUAL=vi crontab -e
#       o <Add your new crontab line>
#       o Save and verify using "crontab -l" 
#       Remember that Cron needs to be enabled in the OpenELEC settings:
#       SYSTEM > OpenELEC > Services > Cron > Enable Cron
#
# To call this immediately on Kodi startup, you might want to also add a call to this 
# script from "/storage/.config/autostart.sh"
#
# NOTE #1: We cannot use "sed -i ..." directly on /etc/resolv.conf because we get the following error:
#		sed: can't create temp file '/etc/resolv.confKLCjum': Read-only file system
#          I'm not sure why, but /etc/resolv.conf is actually a symbolic link to /var/cache/resolv.conf
#          and  fortunately we CAN run sed on that file without a problem.
#
# NOTE #2: Commands including "grep" and "sed" are all links to busybox, which is a single
#          executable, often used in embedded systems to include the basic linux commands.
#          Be aware that these versions of the commands are not always full implementations.
#
# JeremyC Aug 2019

if ! grep 'nameserver 8.8.8.8$' /etc/resolv.conf ; then
	sed -i "s/nameserver.*/nameserver 8.8.8.8/" /var/cache/resolv.conf
fi
