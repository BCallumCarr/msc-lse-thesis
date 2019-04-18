gcloud config list
export PROJECT="stack-exchange-project"
gcloud config set project ${PROJECT}

export NUM_WORKERS="4"
export BUCKET="bucket-brad-project"
export CLUSTER="cluster-brad"

gcloud dataproc clusters create ${CLUSTER} \
--properties=^#^spark:spark.jars.packages=graphframes:graphframes:0.5.0-spark2.1-s_2.11,com.databricks:spark-xml_2.11:0.4.1 \
 --subnet default --zone europe-west2-a --master-machine-type n1-standard-4 \
 --master-boot-disk-size 500 --num-workers=${NUM_WORKERS} --worker-machine-type n1-standard-4 \
 --worker-boot-disk-size 500 --image-version 1.3-deb9 --project=${PROJECT} --bucket=${BUCKET} \
 --initialization-actions 'gs://dataproc-initialization-actions/jupyter/jupyter.sh',\
'gs://dataproc-initialization-actions/python/pip-install.sh','gs://bucket-brad-project/my-actions.sh' \
--metadata 'PIP_PACKAGES=sklearn nltk pandas'

export PORT=8123
export ZONE="europe-west2-a"
export HOSTNAME=cluster-brad-m

gcloud compute ssh ${HOSTNAME} \
    --project=${PROJECT} --zone=${ZONE}  -- \
    -D ${PORT} -N &

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
      --proxy-server="socks5://localhost:${PORT}" \
      --user-data-dir=/tmp/${HOSTNAME}


gcloud dataproc clusters delete cluster-brad
