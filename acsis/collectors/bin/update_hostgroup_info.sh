#!/bin/bash
# update_hostgroup_info.sh 
# Update hostgroup info from host info.
# Runs on aiadm.cern.ch.
# @Author: Jaroslava Schovancova <jaroslava.schovancova@cern.ch>
# 
URL_HOSTGROUP_UPDATE="http://aipanda043.cern.ch/acsis/hostgroups/api/"
DIR_BIN="$(dirname $0)"
DIR_PARENT="${DIR_BIN}/../"
DIR_OUTPUT="${DIR_PARENT}/output/"
DATA_FILE="${DIR_OUTPUT}/hostgroup_info_update_raw.json"

curl -s -i -X POST ${URL_HOSTGROUP_UPDATE} -H "Content-Type: application/json" --data-binary "@${DATA_FILE}"

