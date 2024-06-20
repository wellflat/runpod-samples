#!/bin/sh

echo "start model repository clone"
git lfs install
echo ${MODEL_REPO_URL}
git clone "${MODEL_REPO_URL}"
echo "clone completed"
git checkout "${SUBMODULE_COMMIT_ID}"
ls sample-models/models
echo "start handler"
python3 -u rp_handler.py