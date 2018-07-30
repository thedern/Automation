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
Takes build dir and target env as arguments
Deploys code 
Deploys static after 5 min delay
!Does not restart application servers!

executes deployOnly.sh from same directory
executes pushstaticOnlyv2.py for static content sync

"""


#SCRIPT ARGUMENTS ARE BUILD DIR AND DEPLOY ENVIRONMENT
from sys import argv
script, buildDir, targetEnv = argv
#print "DEBUG argv[1] %s" % argv[1]

#GUARDIAN STATEMENT
if len(argv) == 0:
	print "Usage is <scriptname> <build directory name> <target env> \n
			example: deployOnlyv3.py wcbd-deploy-server-CVWEB_RELEASE_6.14_32725 ecomqa03"
	sys.exit()

devnull = open(os.devnull, 'w')

####################
#### FUNCTIONS #####
####################

#--------------------------------------------------------------------------------------------------------#
#LOGGER

def logger(x):
        logfile = open('/home/wasuser2/buildDeployCVE.log', 'a')
        logfile.write(x)
        logfile.close()


#--------------------------------------------------------------------------------------------------------#
#DEPLOY APPLICATION

def deployApp(buildDir, targetEnv, devnull):
	#print "DEBUG: buildDir is", buildDir
	#print "DEBUG: targetEnv is", targetEnv
	#DEPLOY SCRIPT WRAPPER FOR WCBD-ANT; REQUIRED TO SOURCE UNIX ENVIRONMENT
        process = subprocess.Popen(['./deployOnly.sh', buildDir, targetEnv], stdout=devnull)
        #PROGRAM PAUSE UNTIL DEPLOY IS DONE
        process.wait()
        retCode = process.returncode
        print "DEBUG return code is ", process.returncode

        ###### WAIT POST DEPLOY #####
	print "waiting..."
        time.sleep(600)

	return retCode


#--------------------------------------------------------------------------------------------------------#
#DEPLOY STATIC 

def deployStatic(logger, devnull):
	print "pushing static content"
	#copy2web.sh DOES NOT DECLARE A SHELL; THEREFORE, POPEN MUST CALL A SHELL ELSE EXECUTION WILL ERROR
	stopProcess = subprocess.Popen(['/home/wasuser2/buildDeployCVE/pushstaticOnlyv2.py'])
        stopProcess.wait()
        retCode = stopProcess.returncode
        return retCode


#--------------------------------------------------------------------------------------------------------#

##############
#### MAIN ####
##############

print "deploy started"
depRetCode = deployApp(buildDir, targetEnv, devnull)

if depRetCode == 0:
	msgDeploySuccess =  "deploy successful \n"
        print "DEBUG", msgDeploySuccess
	logger(msgDeploySuccess)
	deptStatCode = deployStatic(logger, devnull, hostName)
	if deptStatCode == 0:
		msgStatSuccess = "static content push executed \n"
		print "DEBUG", msgStatSuccess
		logger(msgStatSuccess)
	else:
		msgStatFail = "static content push failed \n"
		print "DEBUG", msgStatFail
		logger(msgStatFail)

else:
	msgDeployFail = "deploy failed, please check logs"
	print "DEBUG", msgDeployFail
	logger(msgDeployFail)
	
