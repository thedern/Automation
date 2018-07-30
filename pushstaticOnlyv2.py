#!/usr/bin/python

import socket
import sys
import os
import subprocess

"""
NOTES:

Evaluates the host from which the script is executed and runs the corresponding static rsync
script from its correct path on the host.

Live Prod, Live Stage, and Lowers all have different static content rsync script paths and names

Usage:  ./pushstaticOnlyv2.py      Script takes no arguments

""""

devnull = open(os.devnull, 'w')

###################
#### FUNCTIONS ####
###################

#--------------------------------------------------------------------------------------------------------#
#LOGGER

def logger(x):
        logfile = open('/home/wasuser2/buildDeployCVE/buildDeployCVE.log', 'a')
        logfile.write(x)
        logfile.close()


#--------------------------------------------------------------------------------------------------------#
#DEPLOY STATIC LOWER ENV

def deployStaticLower(logger, serverName, devnull):
        staticProcess = subprocess.Popen(['sh','/optware/scripts/static_contents/copy2web.sh'], stdout=devnull)
        staticProcess.wait()
        resultStatic = staticProcess.returncode
        if resultStatic == 0:
                staticMessage = "static content push " +serverName+ " success \n"
                logger(staticMessage)
		print "DEBUG:", staticMessage
        else:
                staticMessage = "static push failed, " +serverName+ "please check \n"
                logger(staticMessage)
		print "DEBUG:", staticMessage
		
#--------------------------------------------------------------------------------------------------------#
#DEPLOY STATIC PROD ENV

def deployStaticProd(logger, devnull):
        staticProcess = subprocess.Popen(['sh','/optware/scripts/static_contents_v7/prd2static_rsync.sh'], stdout=devnull)
        staticProcess.wait()
        resultStatic = staticProcess.returncode
        if resultStatic == 0:
                staticMessage = "static content push in Live Prod, success \n"
                logger(staticMessage)
		print "DEBUG:", staticMessage
        else:
                staticMessage = "static push in Live Prod failed, please check \n"
                logger(staticMessage)
		print "DEBUG:", staticMessage

#--------------------------------------------------------------------------------------------------------#
#DEPLOY STATIC LIVE STAGE ENV

def deployStaticLS(logger, devnull):
        staticProcess = subprocess.Popen(['sh','/optware/scripts/static_contents/stg2static_rsync.sh'], stdout=devnull)
        staticProcess.wait()
        resultStatic = staticProcess.returncode
        if resultStatic == 0:
                staticMessage = "static content push in Live Stage, success \n"
                logger(staticMessage)
		print "DEBUG:", staticMessage
        else:
                staticMessage = "static push in Live Stage failed, please check \n"
                logger(staticMessage)
		print "DEBUG:", staticMessage

#--------------------------------------------------------------------------------------------------------#
def getHostname():
        return socket.gethostname()

#--------------------------------------------------------------------------------------------------------#

##############
#### MAIN ####
##############

serverName =  getHostname()
print "DEBUG servername is", serverName

if serverName == "wcndprd01":
	deployStaticProd(logger, devnull)		

elif serverName == "wcappstg01"	
	deployStaticLS(logger, devnull)
	
else:
	deployStaticLower(logger, serverName, devnull)	

