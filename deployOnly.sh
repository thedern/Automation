#!/bin/bash
#echo "ARG 1 $1"
#echo "ARG 2 $2" 
cd /optware/IBM/WebSphere/V7/CommerceServer70/wcbd/dist/server/$1
echo "DEBUG: current dir is" `pwd`

./wcbd-ant -buildfile wcbd-deploy.xml -Dtarget.env=$2
