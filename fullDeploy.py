
"""
Author:  Darren Smith

Purpose: Deploys commerce application, restarts servers, and executes static content sync.
         It can differentiate between prod and non-prod as well as between clustered and
         standalone environments.

Date:    7/9/2018

Notes:

Due to limitations in wsadmin/jython's ability in interacting with the filesystem, this wrapper uses
python v2.4 (version installed) to deploy the CVE application and push static content while using
separate jython-based scripts for the associated WAS management. More precisely the version of jython
included with WAS7 connot import a number of required python modules such as 'subprocess' due to their
supporting libraries being compiled as C-based shared objects (<libname>.so).

This wrapper script calls the following jython-based scripts for cell managment.

'/home/wasuser2/buildDeployCVE/stopClusterWSAdminv1.py'
'/home/wasuser2/buildDeployCVE/restartWASOnlyWSAdminv1.py'

"""

import time
import sys
import os
import socket

#WAS & JYTHON CANNOT IMPORT THESE MODULES
import datetime
import subprocess
import glob

devnull = open(os.devnull, 'w')
wasBin = '/optware/IBM/WebSphere/V7/AppServer/profiles/cve/bin'
dt = datetime.datetime.now().strftime("%m/%d/%y")

#CAPTURE SCRIPT START TIME
start_time = time.time()

#SCRIPT ARGUMENTS ARE BUILD DIR AND DEPLOY ENVIRONMENT
from sys import argv
script, buildDir, targetEnv = argv
#print "DEBUG argv[1] %s" % argv[1]

#LIST OF CLUSTERED ENVIRONMENTS
clusterList = [ 'ecomdev03', 'ecomqastg03', 'ecomqa03',
		'ecomdev04', 'ecomqastg04', 'ecomqa04'
		'wcappstg01', 'wcappqa01', 'wcndprd01' ]


#### FUNCTIONS ####

#--------------------------------------------------------------------------------------------------------#
#LOGGER

def logger(x):
        logfile = open('/home/wasuser2/buildDeployCVE/buildDeployCVE.log', 'a')
        logfile.write(x)
        logfile.close()


#--------------------------------------------------------------------------------------------------------#
#GET HOSTNAME

def getHostname():
        return socket.gethostname()


#--------------------------------------------------------------------------------------------------------#
#DEPLOY APPLICATION
#TESTED 7/20; /backup/ecomm/sysadm/darren/deployOnly.py

def deployApp(buildDir, targetEnv, devnull):
        #print "DEBUG: buildDir is", buildDir
        #print "DEBUG: targetEnv is", targetEnv
        #DEPLOY SCRIPT WRAPPER FOR WCBD-ANT; REQUIRED TO SOURCE UNIX ENVIRONMENT
        process = subprocess.Popen(['./deployOnly.sh', buildDir, targetEnv], stdout=devnull)
        #PROGRAM PAUSE UNTIL DEPLOY IS DONE
        process.wait()
        retCode = process.returncode
        print "DEBUG return code is ", process.returncode

        ###### WAIT POST DEPLOY ######
        print "waiting..."
        time.sleep(600)

        return retCode


#--------------------------------------------------------------------------------------------------------#
#DEPLOY STATIC LOWER ENV
#TESTED 7/20; /backup/ecomm/sysadm/darren/deployOnly.py

def deployStaticLower(logger, devnull):
	staticProcess = subprocess.Popen(['sh','/optware/scripts/static_contents/copy2web.sh'], stdout=devnull)
        staticProcess.wait()
        resultStatic = staticProcess.returncode
        if resultStatic == 0:
                staticMessage = "static content push success \n"
                logger(staticMessage)
        else:
                staticMessage = "static push failed, please check \n"
                logger(staticMessage)


#--------------------------------------------------------------------------------------------------------#
#DEPLOY STATIC PROD ENV

def deployStaticProd(logger, devnull):
        staticProcess = subprocess.Popen(['sh','/optware/scripts/static_contents_v7/prd2static_rsync.sh'], stdout=devnull)
        staticProcess.wait()
        resultStatic = staticProcess.returncode
        if resultStatic == 0:
                staticMessage = "static content push success \n"
                logger(staticMessage)
        else:
                staticMessage = "static push failed, please check \n"
                logger(staticMessage)

#--------------------------------------------------------------------------------------------------------#
#RESTART DMGR
#TESTED 7/17; /backup/ecomm/sysadm/darren/testPython/restartDMGR.py

def restartDMGR(logger):
	#TO REDIRECT STDOUT TO DEV/NULL
	devnull = open(os.devnull, 'w')

	dmgrBinList = glob.glob('/optware/IBM/WebSphere/V7/AppServer/profiles/D*/bin')
	#GET FIRST ITEM FROM LIST; STRING FOR BINARY PATH
	dmgrBin = dmgrBinList[0]

	stopProcess = subprocess.Popen([dmgrBin+'/stopManager.sh'], stdout=devnull)
	stopProcess.wait()
	resultStop = stopProcess.returncode
	#TEST TO SEE IF DMGR PORT ACTIVE; RETURN CODE '1' MEANS INACTIVE
	test = subprocess.call(['/usr/sbin/lsof','-i',':9075'], stdout=devnull)

	if resultStop == 0 and test == 1:
		dmgrStopMsg = "dmgr stopped sucessfully, restarting \n"
		logger(dmgrStopMsg)
		print "DEBUG", dmgrStopMsg

		startProcess = subprocess.Popen([dmgrBin+'/startManager.sh'], stdout=devnull)	
		startProcess.wait()
		resultStart = startProcess.returncode
		#TEST TO SEE IF DMGR PORT ACTIVE; RETURN CODE '0' MEANS ACTIVE
		test = subprocess.call(['/usr/sbin/lsof','-i',':9075'], stdout=devnull)

		if resultStart == 0 and test == 0:
			dmgrStartMsg = "dmgr restarted sucessfully \n"
			logger(dmgrStartMsg)
			
		else:
			dmgrStartMsg = "dmgr restart failed, please check. Exiting \n"
			logger(dmgrStartMsg)
			print "DEBUG", dmgrStartMsg	
			sys.exit()
	else:
		dmgrStopMsg = "dmgr stop failed, please check. Exiting \n"
		logger(dmgrStopMsg)
		print "DEBUG", dmgrStopMsg
		sys.exit()
		
	
#--------------------------------------------------------------------------------------------------------#
#START WAS VIA WSADMIN (CENTRALIZED)
#TESTED 7/18; /backup/ecomm/sysadm/darren/testPython/restartClusterTest.py

def wasStart(hostName, wasBin):
	
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
#STOP WAS VIA WSADMIN (CENTRALIZED)
#TESTED 7/18; /backup/ecomm/sysadm/darren/testPython/restartClusterTest.py

def stopCluster(wasBin):
	stopProcess = subprocess.Popen([wasBin+'/wsadmin.sh','-lang','jython','-f','/home/wasuser2/buildDeployCVE/stopClusterWSAdminv1.py'])
	stopProcess.wait()
	retCode = stopProcess.returncode
	return retCode

#--------------------------------------------------------------------------------------------------------#

#### MAIN #####
#### DETERMINE HOST ####

logger(dt)
logger(start_time)

hostName = getHostname()
if hostName == 'wcndprd01':
	restartDMGR(logger)

#### DEPLOY TO CLUSTERED ENVIRONMENTS ####

if hostName in clusterList:
	###STOP CLUSTER BEFORE DEPLOY
	stopRetCode = stopCluster(wasBin)

	if stopRetCode == 0:
		###DEPLOY CVE###
		depRetCode = deployApp(buildDir, targetEnv)
	
		if depRetCode == 0:	
			msgDeploySuccess =  "deploy successful \n"
			print "DEBUG", msgDeploySuccess
        		logger(msgDeploySuccess)

			if hostName = 'wcndprd01':
				deployStaticProd(logger)
			else:
				deployStaticLower(logger)
			
			###CALL WSADMIN FOR CLUSTER/SERVER STARTUP
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
			msgDeployFailed = "Length of appCheck is '0', deploy failed/application not running. Please check the logs \n"
        		print "DEBUG", msgDeployFailed
       		 	logger(msgDeployFailed)
        		sys.exit()

	else:
		stopMsg = "Cluster stop script did not successfully execute, please check cluster. \n"
		logger(stopMsg)
		print "DEBUG", stopMsg		
		sys.exit()
		
	
else:
	### DEPLOY CVE TO STANDALONE SERVERS ###

	depRetCode = deployApp(buildDir, targetEnv)

	if depRetCode == 0:
		msgDeploySuccess =  "deploy successful \n"
       	        print "DEBUG", msgDeploySuccess
                logger(msgDeploySuccess)
                deployStaticLower(logger)

                ###CALL WSADMIN FOR CLUSTER/SERVER STARTUP
                startRetCode = wasStart()

		if startRetCode == 0:
                	restartMsg = "restart script successfully executed.\n Check restart log for server states. \n"
                	logger(restartMsg)
               		print "DEBUG", restartMsg
               	else:
               		restartMsg = ""restart script failed, manually check application servers. \n"
               		logger(restartMsg)
               		print "DEBUG", restartMsg
	else:
        	msgDeployFailed = "Length of appCheck is '0', deploy failed/application not running. Please check the logs \n"
                print "DEBUG", msgDeployFailed
                logger(msgDeployFailed)
                sys.exit()


msgTime = ("EXECUTION TIME: \n --- %s seconds ---" % (time.time() - start_time))
print "DEBUG", msgTime
logger(msgTime)
