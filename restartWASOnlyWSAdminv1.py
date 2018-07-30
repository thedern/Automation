"""
Author:  Darren Smith

Purpose: Restarts standalone server instances as well as specific cluster members in 
a cell or all cluster members in a cell depending on stack and enviroment within the stack.

Date:    7/18/2018

Note:
cluster states
'websphere.cluster.partial.start'
'websphere.cluster.partial.stop'
'websphere.cluster.running'
'websphere.cluster.stopped'

***** NOTE THIS SCRIPT IS CALLED BY 'BD_CVE_Wrapper.py' or 'restartClusterTest.py' ****

"""

import time
import socket

#NON-CLUSTERED ENVIRONMENTS
standAloneList = ['ecomdev2','ecomqa2stg01','ecomqa2','wcappqastg01']

#### FUNCTIONS ####

#--------------------------------------------------------------------------------------#
#LOGGER

def logger(x):
        logfile = open('/home/wasuser2/buildDeployCVE/buildDeployCVE.log', 'a')
        logfile.write(x)
        logfile.close()


#--------------------------------------------------------------------------------------#
#GET STANDALONE SERVER STATE; TAKES SERVER MBEAN AS ARGUMENT

def getState(s1):
        print "DEBUG Getting server state"
        return AdminControl.getAttribute(s1, 'state')


#--------------------------------------------------------------------------------------#
#START PROD SERVERS
#ONLY SPECIFIC SERVERS ARE TO BE STARTED, CANNOT START WHOLE CLUSTER IN PROD

def startProdServers(logger):
        prdServers1 = { 'WC_cve_node_nd' : 'server1', 'WC_cve_node' : 'server1',
                'WC_cve_node_02' : 'server1', 'WC_cve_node_03': 'server1',
                'WC_cve_node_04' : 'server1', 'WC_cve_node_05' : 'server1',
                'WC_cve_node_06' : 'server1' }

        prdServers2 = { 'WC_cve_node_06' : 'server2' }

        #ITERATE THROUGH DICTIONARIES AND START SERVERS
	#COMMANS IS: AdminControl.startServer(server, node)

	startServer1Msg = "starting server1 on all live prod nodes in cluster \n"
        logger(startServer1Msg)
        print startServer1Msg

        for key in prdServers1:
                AdminControl.startServer(prdServers1[key], key)

	startServer2Msg = "starting server2 on wcappprd06 only \n"
        logger(startServer2Msg)
        print startServer2Msg

        for key in prdServers2:
                AdminControl.startServer(prdServers2[key], key)


        #time.sleep(600)

#--------------------------------------------------------------------------------------#
#ECOMQA04: START SERVER1 ON NODE1 ONLY

def startPrd04(logger):
        prd04Servers1 = { 'WC_cve_node' : 'server1' }
        #ITERATE THROUGH DICTIONARIES AND START SERVERS

	startServer1Msg = "starting server1 on ecomqa04 node1 \n"
        logger(startServer1Msg)
        print startServer1Msg

        for key in prd04Servers1:
                AdminControl.startServer(prd04Servers1[key], key)


#--------------------------------------------------------------------------------------#
#LIVE STAGE: START NODE1 SERVER ONLY

def startLiveStage(logger):
        LS_Servers1 = { 'WC_cve_node' : 'server1' }

        #LS_Servers2 = { 'WC_cve_node_02' : 'server1' }

        #ITERATE THROUGH DICTIONARIES AND START SERVERS

	startServer1Msg = "starting server1 on live stage node1 \n"
        logger(startServer1Msg)
        print startServer1Msg

        for key in LS_Servers1:
                AdminControl.startServer(LS_Servers1[key], key)


#--------------------------------------------------------------------------------------#
#WCAPPQA01: START NODE1 SERVER ONLY

def startPrd01(logger):
        prd01_Servers1 = { 'WC_cve_node' : 'server1', 'WC_cve_node2' : 'server1' }

        #prd01_Servers2 = { 'WC_cve_node' : 'server2' }

        #ITERATE THROUGH DICTIONARIES AND START SERVERS

	startServer1Msg = "starting server1 on all QA01 nodes in cluster \n"
        logger(startServer1Msg)
        print startServer1Msg

        for key in prd01_Servers1:
                AdminControl.startServer(prd01_Servers1[key], key)


#--------------------------------------------------------------------------------------#
#STARTUP STANDALONE SERVER
#TAKES SERVER AND NODE NAME AS ARGUMENT, MBEAN NOT REQUIRED

def startup(server, node, logger):
	startMsg = "Starting server1 \n"
	logger(startMsg)
        print "DEBUG Starting server"
        AdminControl.startServer(server, node)


#--------------------------------------------------------------------------------------#
#SHUTDOWN STANDALONE SERVER
#TAKES SERVER NAME AS ARGUMENT, MBEAN NOT REQUIRED

def shutdown(server, logger):
	stopMsg = "Stopping server1 \n"
        logger(stopMsg)
        print "DEBUG Stopping server"
        AdminControl.stopServer(server,'immediate')


#--------------------------------------------------------------------------------------#
#STARTS ENTIRE CLUSTER FOR ALL CLUSTERED ENVIRONMENTS NOT SPECIFICALLY NAMED

def startCluster(logger):
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
		#START CLUSTER
		clusterMsg = "starting cluster for " + cell + "\n"
		logger(clusterMsg)
		print "DEBUG", clusterMsg
		AdminControl.invoke(clusterBean, 'start')
		clusterMsg2 = "cluster for " + cell + " started \n"
		logger(clusterMsg2)
		print "DEBUG", clusterMsg2


#--------------------------------------------------------------------------------------#
#GET APPLICAION STATUS

def appStatus():
        return AdminControl.completeObjectName('type=Application,name=WC_cve,*')


#--------------------------------------------------------------------------------------#
#GET HOSTNAME

def getHostname():
        return socket.gethostname()


#--------------------------------------------------------------------------------------#

#### MAIN ####

hostName = getHostname()
if hostName == 'wcndprd01':
	#PROD CLUSTER SHOULD BE DOWN
	startProdServers(logger)
	#CHECK SERVERS, LOG STATE

elif hostName == 'wcappstg01':
	#LS CLUSTER SHOULD BE DOWN
	startLiveStage(logger)

elif hostName == 'ecomqa04':
	#04 CLUSTER SHOULD BE DOWN
	startPrd04(logger)	

elif hostName == 'wcappqa01':
	#01 CLUSTER SHOULD BE DOWN
	startPrd01(logger)

elif hostName in standAloneList:
	#STANDALONE ENV, START SERVER1

        #GET MBEAN
        s1 = AdminControl.completeObjectName('WebSphere:type=Server,*')
        #GET NODE NAME
        node = AdminControl.getAttribute(s1, 'nodeName')
	print 'DEBUG node is', node
        #GET SERVER NAME
        serverName =  AdminControl.getAttribute(s1, 'name')
        status1 = getState(s1)

        if status1  == 'STARTED':
        	msg = "The current state of " + node + " " + serverName + " is " + status1 + " , Restarting..." + "\n"
        	print msg
        	logger(msg)
        	#shutdown WILL WAIT FOR SERVER PROCESS TO DIE AND MBEAN DESTROYED
        	#shutdown(serverName, logger)
        	startup(serverName, node, logger)

else:
	#START ENTIRE CLUSTER
	startCluster(logger)

