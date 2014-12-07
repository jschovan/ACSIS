#!/bin/bash
# fetch_hostgroups.sh 
# Get list of hostgroups from available puppet manifests.
# Runs on aiadm.cern.ch.
# @Author: Jaroslava Schovancova <jaroslava.schovancova@cern.ch>
# 
DIR_BIN="$(dirname $0)"
DIR_PARENT="${DIR_BIN}/../"
DIR_SETTINGS="${DIR_PARENT}/settings/"
DIR_LIB="${DIR_PARENT}/hostgroups/"
DIR_OUTPUT="${DIR_PARENT}/output/"

if [ ! -d ${DIR_OUTPUT} ]; then mkdir -p ${DIR_OUTPUT} ; fi

export PYTHONPATH=${DIR_PARENT}:${PYTHONPATH}

python ${DIR_LIB}/fetch_hostgroups.py ${DIR_SETTINGS}/hostgroups.cfg

