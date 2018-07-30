#!/usr/bin/python


import os
import subprocess
import glob
import sys

"""
NOTES:

Restarts DMGR only Live Prod. Due to limitation in grepping for process in python, using
'lsof' to determine if prod dmgr is listening on its port.  Lower envs use different ports
if port passed in via argument, script can be used against non-prod.  Likelyhood of needing
to restart non-prod dmgr is very remote.

Useage: ./restartPrdDmgr.py	Script takes no arguments

"""

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

#RESTART DMGR

def restartDMGR(logger, devnull):

        dmgrBinList = glob.glob('/optware/IBM/WebSphere/V7/AppServer/profiles/D*/bin')
        #GET FIRST ITEM FROM LIST; STRING FOR BINARY PATH
        dmgrBin = dmgrBinList[0]
	print "DEBUG", dmgrBin
	print "DEBUG stopping dmgr"
	logger("DEBUG stopping dmgr \n")

        stopProcess = subprocess.Popen([dmgrBin+'/stopManager.sh'], stdout=devnull)
        stopProcess.wait()
        resultStop = stopProcess.returncode
        #TEST TO SEE IF DMGR PORT ACTIVE; RETURN CODE '1' MEANS INACTIVE
        test = subprocess.call(['/usr/sbin/lsof','-i',':9043'], stdout=devnull)

        if resultStop == 0 and test == 1:
                dmgrStopMsg = "dmgr stopped sucessfully, restarting \n"
                logger(dmgrStopMsg)
                print "DEBUG", dmgrStopMsg

                startProcess = subprocess.Popen([dmgrBin+'/startManager.sh'], stdout=devnull)
                startProcess.wait()
                resultStart = startProcess.returncode
                #TEST TO SEE IF DMGR PORT ACTIVE; RETURN CODE '0' MEANS ACTIVE
                test = subprocess.call(['/usr/sbin/lsof','-i',':9043'], stdout=devnull)

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
		print "DEBUG", dmgrStartMsg
		sys.exit()

#-------------------------------------------------------------------------------------------#

##############
#### MAIN ####
##############

restartDMGR(logger, devnull)
