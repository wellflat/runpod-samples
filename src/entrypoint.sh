#!/bin/sh

#echo "start model repository clone"
#git lfs install
#echo ${MODEL_REPO_URL}
#git clone "${MODEL_REPO_URL}"
#echo "clone completed"
#cd sample-models
#git checkout "${SUBMODULE_COMMIT_ID}"
#ls models
#cd -

export HF_HUB_ENABLE_HF_TRANSFER=1
huggingface-cli download \
    --token ${HF_TOKEN} \
    --revision ${SUBODULE_COMMIT_ID}
echo "start handler"
python3 -u rp_handler.py