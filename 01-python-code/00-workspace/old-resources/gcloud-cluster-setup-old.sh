## set project beforehand
gcloud config list
export PROJECT="stack-exchange-project"
gcloud config set project ${PROJECT}

## set variables beforehand
export NUM_WORKERS="0"
export BUCKET="bucket-brad-project"
export CLUSTER="cluster-brad"

## spin up cluster
gcloud dataproc clusters create ${CLUSTER} \
--properties=^#^spark:spark.jars.packages=com.databricks:spark-xml_2.11:0.4.1 \
 --subnet default --zone europe-west2-a --master-machine-type n1-standard-2 \
 --master-boot-disk-size 500 --num-workers=${NUM_WORKERS} --worker-machine-type n1-highmem-8 \
 --worker-boot-disk-size 500 --image-version 1.3-deb9 --project=${PROJECT} --bucket=${BUCKET} \
 --initialization-actions 'gs://dataproc-initialization-actions/jupyter/jupyter.sh',\
'gs://dataproc-initialization-actions/python/pip-install.sh','gs://bucket-brad-project/bash-files/my-actions.sh' \
--metadata 'PIP_PACKAGES=sklearn nltk pandas'


## connect to jupyter notebook
export PORT=8123
export ZONE="europe-west2-a"
export HOSTNAME=cluster-brad-m

gcloud compute ssh ${HOSTNAME} \
    --project=${PROJECT} --zone=${ZONE}  -- \
    -D ${PORT} -N &

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
      --proxy-server="socks5://localhost:${PORT}" \
      --user-data-dir=/tmp/${HOSTNAME}
#http://cluster-brad-m:8123

--------------------------------------------------------------------------------

## DELETE clusters after use!
gcloud dataproc clusters delete cluster-brad

#gcloud components update --version 230.0.0
