#!/usr/bin/python

import time
import os
import socket
import subprocess
import sys

#MENU

print "\n", "@" * 24
string = " CVE DEPLOY MENU "
 
new_string = string.center(24, '*')
print new_string, "\n", "@" * 24

dt = datetime.datetime.now().strftime("%m/%d/%y")

#CAPTURE SCRIPT START TIME
start_time = time.time()

####################
#### FUNCTIONS #####
####################

#-------------------------------------------------------------------------------#
#LOGGER

def logger(x):
        logfile = open('/home/wasuser2/buildDeployCVE/buildDeployCVE.log', 'a')
        logfile.write(x)
        logfile.close()


#-------------------------------------------------------------------------------#
def fullDeploy(buildDir, logger):
	pass
	print "full deploy #1\nReturning to Menu"

	buildDir = raw_input('enter build directory: ')

        ##TODO: ERROR CHECK HERE

        targetEnv = raw_input('enter environment: ')

        ##TODO: ERROR CHECK HERE


	#!!!!
        #TODO: NEED TO PASS ARGUMENTS 'DIR' and 'ENV' TEST SYNTAX
        #!!!!
        #TODO: REVIEW FULLDEPLOY AND ENSURE CORRECTED 

        deployFullProcess = subprocess.Popen(['/home/wasuser2/buildDeployCVE/fullDeploy.py' builDir, targetEnv])
        deployFullProcess.wait()
        resultFull = deployFullProcess.returncode
        if resultFull == 0:
                fullDeployMessage = "full deploy success \n"
                logger(fullDeployMessage)
        else:
                fullDeployMessage = "full deploy, please check \n"
                logger(fullDeployMessage)


	options_display()
	
#-------------------------------------------------------------------------------#
def deployOnly(logger):
	pass
        #print "deploy only #2\nReturning to Menu"

	buildDir = raw_input('enter build directory: ')

	##TODO: ERROR CHECK HERE

	targetEnv = raw_input('enter environment: ')

	##TODO: ERROR CHECK HERE
	
	#!!!!
	#TODO: NEED TO PASS ARGUMENTS 'DIR' and 'ENV' TEST SYNTAX
	#!!!!

	deployOnlyProcess = subprocess.Popen(['/home/wasuser2/buildDeployCVE/deployOnlyv3.py' builDir, targetEnv])
        deployOnlyProcess.wait()
        resultDeployOnly = deployOnlyProcess.returncode
        if resultDeployOnly == 0:
                DeployOnlyMessage = "deploy only  success \n"
                logger(DeployOnlyMessage)
        else:
                DeployOnlyMessage = "deploy only, please check \n"
                logger(DeployOnlyMessage)

        options_display()

#-------------------------------------------------------------------------------#
def pushStatic(logger):
	pass
        #print "push static #3\nReturning to Menu"

        staticProcess = subprocess.Popen(['/home/wasuser/buildDeployCVE/pushstaticOnlyv2.py'])
        staticProcess.wait()
        resultStatic = staticProcess.returncode
        if resultStatic == 0:
                staticMessage = "static content push success \n"
                logger(staticMessage)
        else:
                staticMessage = "static push failed, please check \n"
                logger(staticMessage)
        options_display()

#-------------------------------------------------------------------------------#
def stopCluster(logger):
	pass
        #print "stop cluster #4\nReturning to Menu"

	stopProcess = subprocess.Popen(['/home/wasuser/buildDeployCVE/stopClusterWSADminv1.py'])
        stopProcess.wait()
        resultStop = stopProcess.returncode
        if resultStop == 0:
                stopMcessage = "cluster stop success \n"
                logger(stopMcessage)
        else:
                stopMcessage = "cluster stop failed, please check \n"
                logger(stopMcessage)

        options_display()

#-------------------------------------------------------------------------------#
def restart():
	pass
        #print "start cluster or restart standalone #5\nReturning to Menu"
	
	restartProcess = subprocess.Popen(['/home/wasuser/buildDeployCVE/restartClusterOnly.py'])
        restartProcess.wait()
        resultRestart = restartProcess.returncode
        if resultRestart == 0:
                restartMessage = "restart of WAS success \n"
                logger(restartMessage)
        else:
                restartMessage = "restart failed, please check \n"
                logger(restartMessage)

        options_display()

#-------------------------------------------------------------------------------#
def restartDmgr():
	pass
	#print "restart of dmgr #6\nReturning to Menu":

	dmgrProcess = subprocess.Popen(['/home/wasuser/buildDeployCVE/restartPrdDmgr.py'])
        dmgrProcess.wait()
        resultDmgr = restartProcess.returncode
        if resultDmgr == 0:
                dmgrMessage = "restart of DMGR success \n"
                logger(dmgrMessage)
        else:
                dmgrMessage = "restart of DMGR failed, please check \n"
                logger(dmgrMessage)

        options_display()
        print "restart Prod dmgr #6\Returning to Menun"
        options_display()

#-------------------------------------------------------------------------------#
#OPTIONS DISPLAY
def options_display():
	print "\n", "*" * 50, "\n"
	print "OPTIONS: \n" 

	options = ['1. Full Deploy/Restart',
		   '2. Deploy CVE Only',
	           '3. Push Static Only',
	           '4. Stop Cluster Only',
	           '5. Start Cluster/Restart Standalone Only',
		   '6. Restart Prod Dmgr Only',
		   '7. Exit'] 

	#print "DEBUG", len(options)

	for option in options:
		print "\t",option

	print "\n", "*" * 50, "\n"

	test = raw_input("Enter Selection by its Associated Number: \n")
	if test != None:
		test = int(test)
		print "\nyou selected: ",test, "\n"
	
		if test < 0 or test > len(options):
			print "ERROR: enter a number corresponding to the choices listed above \n"	
			options_display()

		elif test == 1:
			fullDeploy()	
		elif test == 2:
			deployOnly()
		elif test == 3:
			pushStatic()
		elif test == 4:
			stopCluster()
		elif test == 5:
			restart()
		elif test == 6:
			restartDmgr()
		elif test == 7:
			print "EXITING"
			sys.exit()
	else:
		options_display()
#-------------------------------------------------------------------------------#

##############
#### MAIN ####
##############

options_display()

msgTime = ("EXECUTION TIME: \n --- %s seconds ---" % (time.time() - start_time))
print "DEBUG", msgTime
logger(msgTime)

