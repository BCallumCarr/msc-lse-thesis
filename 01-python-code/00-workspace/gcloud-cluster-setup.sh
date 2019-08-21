## set project beforehand
gcloud config list
export PROJECT="stack-exchange-project"
gcloud config set project ${PROJECT}

## set variables beforehand
export NUM_WORKERS="2"
export BUCKET="bucket-brad-project"
export CLUSTER="cluster-jup"

## spin up cluster with beta and 1.4 version to enable component gateway
gcloud beta dataproc clusters create ${CLUSTER} \
 --enable-component-gateway \
 --subnet default --zone europe-west2-a --master-machine-type n1-highmem-32 \
 --master-boot-disk-size 500 --num-workers=${NUM_WORKERS} --worker-machine-type n1-highmem-8 \
 --worker-boot-disk-size 500 --image-version 1.4 --project=${PROJECT} --bucket=${BUCKET} \
 --optional-components=ANACONDA,JUPYTER \
 --initialization-actions 'gs://dataproc-initialization-actions/python/pip-install.sh',\
'gs://bucket-brad-project/bash-files/my-actions.sh' \
 --metadata 'PIP_PACKAGES=nltk pandas'

# jupyter initialisation isn't working
#'gs://dataproc-initialization-actions/jupyter/jupyter.sh', \

## connect to jupyter notebook
export PORT=8123
export ZONE="europe-west2-a"
export HOSTNAME=cluster-jup-m
export PROJECT="stack-exchange-project"
gcloud config set project ${PROJECT}

gcloud compute ssh ${HOSTNAME} \
    --project=${PROJECT} --zone=${ZONE}  -- \
    -D ${PORT} -N &

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
      --proxy-server="socks5://localhost:${PORT}" \
      --user-data-dir=/tmp/${HOSTNAME} http://${HOSTNAME}:8123

--------------------------------------------------------------------------------

## DELETE clusters after use!
gcloud dataproc clusters delete cluster-brad

#################################
### EXTRA stuff
#################################

# to connext with tim piggot-wolff's method
#ssh -L 8888:localhost:8888 bcallumcarr_gmail_com@35.197.251.199 -A

# if you get "baddies" trying to intercept you error
#cd
#rm -rf .ssh/
#ssh-keygen -t rsa -b 4096 -C "bcallumcarr@gmail.com"
#gcloud compute os-login ssh-keys add --key-file ~/.ssh/id_rsa.pub

# to install python3 pip
#sudo apt install python3-pip

#gcloud components update --version 230.0.0
#problem download for jup-intil'zn: qt-5.9.6
