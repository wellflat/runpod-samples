#!/bin/sh

echo "start model repository clone"
git lfs install
echo ${MODEL_REPO_URL}
git clone "${MODEL_REPO_URL}"
echo "clone completed"
ls sample-models/models
echo "start handler"
python3 -u rp_handler.py