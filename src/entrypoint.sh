#!/bin/sh

echo "start model repository clone"
git lfs install
echo ${MODEL_REPO_URL}
git clone "${MODEL_REPO_URL}"
echo "clone completed"
cd sample-models
git checkout "${SUBMODULE_COMMIT_ID}"
ls models
echo "start handler"
python3 -u rp_handler.py