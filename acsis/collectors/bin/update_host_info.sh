#!/bin/bash
# update_host_info.sh 
# Update host info.
# Runs on aiadm.cern.ch.
# @Author: Jaroslava Schovancova <jaroslava.schovancova@cern.ch>
# 
URL_HOST_UPDATE="http://aipanda043.cern.ch/acsis/hosts/api/"
DIR_BIN="$(dirname $0)"
DIR_PARENT="${DIR_BIN}/../"
DIR_OUTPUT="${DIR_PARENT}/output/"
DATA_FILE="${DIR_OUTPUT}/host_info_raw.json"

curl -s -i -X POST ${URL_HOST_UPDATE} -H "Content-Type: application/json" --data-binary "@${DATA_FILE}"

