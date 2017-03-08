#-------------------------------------------------
#  Script to send command(s) to Cisco Device(s)
#  Commands taken from file "commandlist.txt"
#  IP Address list taken from file "ip_list.txt"
#  Written by aslam@compnet.co.id
#-------------------------------------------------

from netmiko import ConnectHandler
import sys, time
import argparse
from threading import Thread

#-----------------------------------------------
# Usage()
#     This function will print the usage
#-----------------------------------------------
def usage():

   print "Usage: pm.exe <options>"
   print "\n"
   print "REQUIRED OPTIONS:"
   #print "   -h  --host <hostname|ip>   = hostname or ip address"
   print "   -u  --user <username>      = username to login with"
   print "   -p --password <password>      = password for login"
   print "\n"
   print "Other OPTIONS:"
   print "   -e --enable <enable password> = Enable password"
   print "\n"

#-----------------------------------------------
# ios_connect()
#     Connect to device and return an output
#-----------------------------------------------

def ios_connect(username="", password="",commands="", enablepw='!', ip_address=""):

    device = dict()
    device['username'] = username   
    device['password'] = password
    device['secret'] = enablepw
    device['ip'] = ip_address
  
    output_file = ip_address+".txt"
    fo = open(output_file,"w")
    try:
        device['device_type'] = 'cisco_ios_ssh'
        net_connect = ConnectHandler(**device)
        time.sleep(3)
    except:
        try:
            device['device_type'] = 'cisco_ios_telnet'
            net_connect = ConnectHandler(**device)
            time.sleep(3)
        except:
            hasil = "Error connecting "
            fo.write(hasil)
            return False
    else:        
        outputs = []        
        if device['secret'] != '!':
            net_connect.enable()
        
        for command in commands:    
            output = net_connect.send_command_expect(command)
            outputs.append(output)
        
        hasil = '\n'.join(outputs)
        fo.write(hasil)
        fo.close()
        return outputs
        net_connect.clear_buffer()
        net_connect.disconnect()
        
        

import logging

paramiko_logger = logging.getLogger('paramiko.transport')
if not paramiko_logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s | %(levelname)-8s| PARAMIKO: '
                          '%(lineno)03d@%(module)-10s| %(message)s')
        )
    paramiko_logger.addHandler(console_handler)
    
try:
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-u','--user', help='Device Username', required=True)
    parser.add_argument('-p','--password', help='Device Password', required=True)
    #parser.add_argument('-i','--ip', help='Device IP Address', required=True)
    parser.add_argument('-e','--enable',default='!')
    args = vars(parser.parse_args())
except:
    usage()
    sys.exit()
else:
    fh = open("commandlist.txt")
    commands = fh.readlines()

    fip = open("ip_list.txt")
    ips = fip.readlines()
    
    for ip in ips:
        ip = ip.rstrip()
        t=Thread(target=ios_connect, args=(args['user'],args['password'],commands,args['enable'],ip))
        t.start()

'''        
        output = ios_connect(args['user'],args['password'],commands,args['enable'],ip)
        if output is False:
            print "Error Connecting to ",ip
            fo.write ("Error Connecting to ",ip)
        else:
            hasil = '\n'.join(output)
            print "Capturing ",ip,"..."
        fo.write(hasil)
'''        