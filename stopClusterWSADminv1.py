"""
Author:  Darren Smith

Purpose:  Detects if a cluster is running and stops it

Date:    7/11/2018

Note: cluster states
'websphere.cluster.partial.start'
'websphere.cluster.partial.stop'
'websphere.cluster.running'
'websphere.cluster.stopped'

Note: standalone servers are not to be stopped, need to be running to deploy code.

***** NOTE THIS SCRIPT IS CALLED BY 'BD_CVE_Wrapper.py' or 'restartClusterTest.py' ****

"""

import time

#### FUNCTIONS ####
#------------------------------------------------------------------------#
#LOGGER

def logger(x):
        logfile = open('/home/wasuser2/buildDeployCVE/buildDeployCVE.log', 'a')
        logfile.write(x)
        logfile.close()

#------------------------------------------------------------------------#

def shutdownCluster(clusterBean):
        x = None
        print "DEBUG Stopping Cluster"
        AdminControl.invoke(clusterBean, 'stop')
        #CHECK TO SEE CLUSTER HAS STOPPED
        while x != "websphere.cluster.stopped":
		print "sleeping"
                time.sleep(5)
                x = AdminControl.getAttribute(clusterBean, 'state')
		print "DEBUG", x

#------------------------------------------------------------------------#

#### MAIN ####

#GET CELL NAME
cell = AdminControl.getCell()
print "DEBUG cell is", cell

#TEST TO SEE IF CLUSTER EXISTS BY OBTAINING CLUSTER_ID
clusterID = AdminConfig.list('ServerCluster', AdminConfig.getid( '/Cell:' + cell))
print "DEBUG cluster name is", clusterID

#CHECK IF CLUSTER EXISTS
if len(clusterID) > 0:
        #GET CLUSTERNAME ONLY - USES CLUSTERID
        clusterName =  AdminConfig.showAttribute(clusterID, 'name')
        #GET CLUSTER MBEAN - USES CELL AND CLUSTERNAME
        clusterBean = AdminControl.completeObjectName('cell='+cell+',type=Cluster,name='+clusterName+',*')
        #GET CLUSTER STATE - USES CLUSTERMBEAN
        clusterState  = AdminControl.getAttribute(clusterBean, 'state')

        if clusterState != 'websphere.cluster.stopped':
                #STOP CLUSTER BEFORE DEPLOY
		msgDown1 = "cluster running, stopping"
		logger(msgDown1)
		print "DEBUG", msgDown1
                shutdownCluster(clusterBean)
                msgDown2 =  "cluster is down \n"
		logger(msgDown2)
                print "DEBUG ", msgDown2

else:
	noClusterMsg = "No cluster located, returning to main script"
	logger(noClusterMsg)
	print "DEBUG", noClusterMsg

	
