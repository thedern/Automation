#!/usr/bin/python

import time
import sys
import os
import socket

#WAS & JYTHON CANNOT IMPORT THESE MODULES
import datetime
import subprocess
import glob

"""
NOTES:

Restarts clusters identified by hosts inclued in 'clusterList'.

Usage ./restartClusterOnly.py	Script takes no arguments

"""



#LIST OF CLUSTERED ENVIRONMENTS
clusterList = [ 'ecomdev03', 'ecomqastg03', 'ecomqa03',
                'ecomdev04', 'ecomqastg04', 'ecomqa04'
                'wcappstg01', 'wcappqa01', 'wcndprd01' ]

#WAS BIN DIR
wasBin = '/optware/IBM/WebSphere/V7/AppServer/profiles/cve/bin'

####################
#### FUNCTIONS #####
####################

#--------------------------------------------------------------------------------------------------------#
#LOGGER

def logger(x):
        logfile = open('/home/wasuser2/buildDeployCVE/buildDeployCVE.log', 'a')
        logfile.write(x)
        logfile.close()

#--------------------------------------------------------------------------------------------------------#

#STOP WAS VIA WSADMIN (CENTRALIZED)

def stopCluster(wasBin):
	print "stopping cluster"
        stopProcess = subprocess.Popen([wasBin+'/wsadmin.sh','-lang','jython','-f','/home/wasuser2/buildDeployCVE/stopClusterWSAdminv1.py'])
        stopProcess.wait()
	print "stop process complete, returning"
	retCode = stopProcess.returncode
        return retCode

#--------------------------------------------------------------------------------------------------------#
#GET HOSTNAME

def getHostname():
        return socket.gethostname()

#--------------------------------------------------------------------------------------------------------#
#START WAS VIA WSADMIN (CENTRALIZED)

def wasStart(hostName, wasBin):

	print "starting cluster"

        if hostName == 'wcappqa01':
                restartProcess = subprocess.Popen([wasBin+'/wsadmin.sh','-lang','jython','-user','configadmin','-password','CVc0m@dm1n','-f','/home/wasuser2/buildDeployCVE/restartWASOnlyv1.py'])

        elif  hostName == 'ecomqastg02' or hostName == 'ecomqa2':
                restartProcess = subprocess.Popen([wasBin+'/wsadmin.sh','-lang','jython','-user','drsmith','-password','advance1','-f','/home/wasuser2/buildDeployCVE/restartWASOnlyv1.py'])

        else:
                restartProcess = subprocess.Popen([wasBin+'/wsadmin.sh','-lang','jython','-f','/home/wasuser2/buildDeployCVE/restartWASOnlyWSAdminv1.py'])
                restartProcess.wait()
		retCode = restartProcess.returncode
                return retCode

#--------------------------------------------------------------------------------------------------------#

##############
#### MAIN ####
##############

print "Stopping"
hostName = getHostname()
print hostName


if hostName in clusterList:
        ###STOP CLUSTER BEFORE DEPLOY
        stopRetCode = stopCluster(wasBin)
	print "stopRetCode is ", stopRetCode

        if stopRetCode == 0:

		startRetCode = wasStart(hostName, wasBin)

        	if startRetCode == 0:
	        	restartMsg = "restart script successfully executed.\n Check restart log for server states. \n"
	       		logger(restartMsg)
	        	print "DEBUG", restartMsg
        	else:
	        	restartMsg = "restart script failed, manually check application servers. \n"
	        	logger(restartMsg)
	        	print "DEBUG", restartMsg

	else:
		stopMsg = "Cluster stop script did not successfully execute, please check cluster. \n"
        	logger(stopMsg)
        	print "DEBUG", stopMsg
