#!/bin/sh
# 2024/07/02

export HF_HUB_ENABLE_HF_TRANSFER=1
USER=wellflat
for line in `cat submodule_list.csv`
do
    COMMIT_ID=`echo $line | cut -d',' -f1`
    REPO=`echo $line | cut -d',' -f2`
    echo "$REPO => $COMMIT_ID"
    huggingface-cli download \
        ${USER}/${REPO} \
        --token ${HF_TOKEN} \
        --revision ${COMMIT_ID}
done

echo "start handler"
python3 -u rp_handler.py