#!/bin/bash
# fetch_host_info.sh 
# Get list of hosts in hostgroups.
# Runs on aiadm.cern.ch.
# @Author: Jaroslava Schovancova <jaroslava.schovancova@cern.ch>
# 
DIR_BIN="$(dirname $0)"
DIR_PARENT="${DIR_BIN}/../"
DIR_SETTINGS="${DIR_PARENT}/settings/"
DIR_LIB="${DIR_PARENT}/hosts/"
DIR_OUTPUT="${DIR_PARENT}/output/"

if [ ! -d ${DIR_OUTPUT} ]; then mkdir -p ${DIR_OUTPUT} ; fi

export PYTHONPATH=${DIR_PARENT}:${PYTHONPATH}

python ${DIR_LIB}/fetch_host_info.py ${DIR_SETTINGS}/host_info.cfg

