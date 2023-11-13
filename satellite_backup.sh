#!/bin/bash
DEST=/backup
if [[ $(date +%d) == 28  ]];then
	satellite-maintain backup offline --assumeyes "$DEST"
else
	if [[ $(date +%w) == 0  ]];then
		LAST=$(ls -td -- $DEST/*/ | head -n 1)
	        satellite-maintain backup offline --assumeyes --incremental "$LAST" "$DEST"
	fi
fi



